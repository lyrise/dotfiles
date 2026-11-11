from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
import re

from sudachipy import Dictionary, SplitMode


@dataclass(frozen=True)
class Finding:
    start: int
    end: int
    text: str
    line: int
    column: int
    detectors: tuple[str, ...]
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class CheckResult:
    text_length: int
    chinese_specific_count: int
    chinese_specific_ratio: float
    findings: tuple[Finding, ...]
    suppressed_count: int = 0

    @property
    def contaminated(self) -> bool:
        return bool(self.findings)


@dataclass(frozen=True)
class _RawFinding:
    start: int
    end: int
    detectors: tuple[str, ...]
    reasons: tuple[str, ...]


# 漢字（CJK統合漢字・拡張A・互換漢字）。仮名や記号は含まない。
_HAN = re.compile(r"[々一-鿿㐀-䶿豈-﫿]")
_KANA = re.compile(r"[ぁ-ゟァ-ヿｦ-ﾟ]")

# 中国語文の判定から除外する行。見出し・箇条書き・表・引用・コードフェンス・番号付き行。
_NON_PROSE_LINE = re.compile(r"^\s*(?:[#>*+|=-]|\d+[.)]|```|~~~)")
_SENTENCE_BOUNDARY = re.compile(r"[。．！？!?…]")

# 中国語文と判定する漢字数の下限。4字にすると四字熟語の体言止めを誤検出する。
_SENTENCE_MIN_HAN = 5
# 日本語の文に必ず現れる品詞。ひとつでもあれば中国語文とは見なさない。
_JAPANESE_ONLY_POS = frozenset({"助詞", "助動詞"})


@lru_cache(maxsize=1)
def _simplified_chars() -> frozenset[str]:
    resource = files("japanese_checker").joinpath("data", "simplified_chars.txt")
    characters: set[str] = set()
    for code_point, character in _read_data(resource, columns=2):
        _verify_code_point(code_point, character)
        characters.add(character)
    return frozenset(characters)


@lru_cache(maxsize=1)
def _kyujitai_chars() -> dict[str, str]:
    resource = files("japanese_checker").joinpath("data", "kyujitai_chars.txt")
    mapping: dict[str, str] = {}
    for code_point, old, current in _read_data(resource, columns=3):
        _verify_code_point(code_point, old)
        mapping[old] = current
    return mapping


def _read_data(resource: Traversable, columns: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in resource.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != columns:
            raise ValueError(f"data format mismatch: {line}")
        rows.append(fields)
    return rows


def _verify_code_point(code_point: str, character: str) -> None:
    if ord(character) != int(code_point.removeprefix("U+"), 16):
        raise ValueError(f"character data mismatch: {code_point} {character}")


@lru_cache(maxsize=1)
def _tokenizer():
    return Dictionary(dict="small").create()


@lru_cache(maxsize=1)
def load_words(path: str | Path) -> tuple[str, ...]:
    words: list[str] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        word, *_ = line.split("\t")
        words.append(word)
    return tuple(words)


def _allowed_spans(text: str, allow_words: tuple[str, ...]) -> list[tuple[int, int]]:
    """許容語が本文に実際に出現する区間を返す。

    語そのものではなく出現位置で抑制するため、「東京大学」を登録しても
    別の場所に単独で現れる「東」は検出されたままになる。
    """
    spans: list[tuple[int, int]] = []
    for word in allow_words:
        if not word:
            continue
        start = 0
        while (index := text.find(word, start)) >= 0:
            spans.append((index, index + len(word)))
            start = index + 1
    return spans


def _is_allowed(finding: _RawFinding, spans: list[tuple[int, int]]) -> bool:
    return any(start <= finding.start and finding.end <= end for start, end in spans)


def _line_and_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    return line, offset - previous_newline


def _merge_findings(findings: list[_RawFinding]) -> list[_RawFinding]:
    if not findings:
        return []

    ordered = sorted(findings, key=lambda finding: (finding.start, finding.end))
    merged = [ordered[0]]
    for finding in ordered[1:]:
        current = merged[-1]
        if finding.start < current.end:
            merged[-1] = _RawFinding(
                start=current.start,
                end=max(current.end, finding.end),
                detectors=tuple(sorted(set(current.detectors + finding.detectors))),
                reasons=tuple(dict.fromkeys(current.reasons + finding.reasons)),
            )
        else:
            merged.append(finding)
    return merged


def _detect_characters(text: str) -> list[_RawFinding]:
    simplified = _simplified_chars()
    kyujitai = _kyujitai_chars()
    findings: list[_RawFinding] = []
    for index, character in enumerate(text):
        if character in simplified:
            findings.append(
                _RawFinding(
                    start=index,
                    end=index + 1,
                    detectors=("simplified",),
                    reasons=("中国語の簡体字",),
                )
            )
        elif character in kyujitai:
            findings.append(
                _RawFinding(
                    start=index,
                    end=index + 1,
                    detectors=("kyujitai",),
                    reasons=(f"「{kyujitai[character]}」の旧字体（中国語の繁体字）",),
                )
            )
    return findings


def _detect_unknown_words(text: str) -> list[_RawFinding]:
    """日本語の辞書で説明できない漢字語を検出する。

    繁体字語（這個・獻身）や日本語に無い漢語（靠近）が未知語として現れる。
    数詞とラテン文字・仮名だけの未知語は日本語でも普通に出るため除く。
    """
    tokenizer = _tokenizer()
    findings: list[_RawFinding] = []
    for line, offset in _iter_lines(text):
        for morpheme in tokenizer.tokenize(line, SplitMode.C):
            surface = morpheme.surface()
            if not morpheme.is_oov() or not _HAN.search(surface):
                continue
            if morpheme.part_of_speech()[1] == "数詞":
                continue
            start = offset + morpheme.begin()
            findings.append(
                _RawFinding(
                    start=start,
                    end=start + len(surface),
                    detectors=("unknown-word",),
                    reasons=("日本語の辞書にない漢字語",),
                )
            )
    return findings


def _detect_chinese_sentences(text: str) -> list[_RawFinding]:
    """日中共通の漢字だけで書かれた中国語の文を検出する。

    日本語の文は必ず助詞か助動詞を伴う。漢字が続くだけで仮名も助詞も無い文は
    日本語として成立しない。ただし見出しや箇条書きや題名は文ではないため、
    句点で終わっていない断片と、行の形が散文でないものは対象から外す。
    """
    tokenizer = _tokenizer()
    findings: list[_RawFinding] = []
    for line, offset in _iter_lines(text):
        if _NON_PROSE_LINE.match(line):
            continue
        for sentence, sentence_offset, terminated in _iter_sentences(line):
            if not terminated:
                continue
            if len(_HAN.findall(sentence)) < _SENTENCE_MIN_HAN:
                continue
            if _KANA.search(sentence):
                continue
            morphemes = tokenizer.tokenize(sentence, SplitMode.C)
            if any(m.part_of_speech()[0] in _JAPANESE_ONLY_POS for m in morphemes):
                continue
            start = offset + sentence_offset
            findings.append(
                _RawFinding(
                    start=start,
                    end=start + len(sentence),
                    detectors=("chinese-sentence",),
                    reasons=("助詞も仮名も無い漢字の連なり。日本語の文として成立しない",),
                )
            )
    return findings


def _detect_deny_words(text: str, deny_words: tuple[str, ...]) -> list[_RawFinding]:
    findings: list[_RawFinding] = []
    for phrase in deny_words:
        if not phrase:
            continue
        start = 0
        while (index := text.find(phrase, start)) >= 0:
            findings.append(
                _RawFinding(
                    start=index,
                    end=index + len(phrase),
                    detectors=("custom-deny",),
                    reasons=("検出語録に登録された中国語句",),
                )
            )
            start = index + 1
    return findings


def _iter_lines(text: str):
    offset = 0
    for line in text.splitlines(keepends=True):
        yield line.rstrip("\r\n"), offset
        offset += len(line)


def _iter_sentences(line: str):
    """行を文に切り、句点で終わっていたかどうかを添えて返す。

    句点の無い断片は題名・見出し・表のセルであって文ではない。
    """
    start = 0
    for index, character in enumerate(line):
        if _SENTENCE_BOUNDARY.match(character):
            yield from _trimmed(line, start, index, terminated=True)
            start = index + 1
    yield from _trimmed(line, start, len(line), terminated=False)


def _trimmed(line: str, start: int, end: int, terminated: bool):
    segment = line[start:end]
    stripped = segment.strip()
    if stripped:
        offset = start + segment.index(stripped)
        yield stripped, offset, terminated


def check_text(
    text: str,
    allow_words: tuple[str, ...] | list[str] = (),
    deny_words: tuple[str, ...] | list[str] = (),
) -> CheckResult:
    raw_findings = (
        _detect_characters(text)
        + _detect_unknown_words(text)
        + _detect_chinese_sentences(text)
        + _detect_deny_words(text, tuple(deny_words))
    )

    spans = _allowed_spans(text, tuple(allow_words))
    findings: list[Finding] = []
    suppressed_count = 0
    for finding in _merge_findings(raw_findings):
        if _is_allowed(finding, spans):
            suppressed_count += 1
            continue
        line, column = _line_and_column(text, finding.start)
        findings.append(
            Finding(
                start=finding.start,
                end=finding.end,
                text=text[finding.start : finding.end],
                line=line,
                column=column,
                detectors=finding.detectors,
                reasons=finding.reasons,
            )
        )

    specific_chars = _simplified_chars() | _kyujitai_chars().keys()
    specific_count = sum(character in specific_chars for character in text)
    ratio = specific_count / len(text) if text else 0.0
    return CheckResult(
        text_length=len(text),
        chinese_specific_count=specific_count,
        chinese_specific_ratio=ratio,
        findings=tuple(findings),
        suppressed_count=suppressed_count,
    )
