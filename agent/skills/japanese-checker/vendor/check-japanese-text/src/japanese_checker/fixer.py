from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from japanese_checker.checker import Finding, _line_and_column

FLAG_ONLY = "-"


@dataclass(frozen=True)
class FixEntry:
    wrong: str
    right: str
    reason: str

    @property
    def flag_only(self) -> bool:
        return self.right == FLAG_ONLY

    @property
    def label(self) -> str:
        return f"{self.wrong}→{self.right}"


def load_fix_words(path: str | Path) -> tuple[FixEntry, ...]:
    entries: list[FixEntry] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 2 or not fields[0] or not fields[1]:
            raise ValueError(f"fix words format mismatch: {line}")
        reason = fields[2] if len(fields) > 2 else ""
        entries.append(FixEntry(wrong=fields[0], right=fields[1], reason=reason))
    return tuple(entries)


def apply_fixes(
    text: str, entries: tuple[FixEntry, ...]
) -> tuple[str, dict[str, int], tuple[Finding, ...]]:
    """訂正語録に従って本文を書き換え、適用件数と報告専用の発見を返す。

    報告専用（`正` が `-`）の発見は、置換で消えても困るため
    訂正前の本文に対して探す。位置の行・列も訂正前の値になる。
    """
    fixed = text
    applied: dict[str, int] = {}
    for entry in entries:
        if entry.flag_only:
            continue
        count = fixed.count(entry.wrong)
        if count:
            fixed = fixed.replace(entry.wrong, entry.right)
            applied[entry.label] = applied.get(entry.label, 0) + count

    flags: list[Finding] = []
    for entry in entries:
        if not entry.flag_only:
            continue
        start = 0
        while (index := text.find(entry.wrong, start)) >= 0:
            line, column = _line_and_column(text, index)
            flags.append(
                Finding(
                    start=index,
                    end=index + len(entry.wrong),
                    text=entry.wrong,
                    line=line,
                    column=column,
                    detectors=("fix-flag",),
                    reasons=(entry.reason or "訂正語録の報告専用行",),
                )
            )
            start = index + 1
    return fixed, applied, tuple(flags)
