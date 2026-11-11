"""同梱データ（簡体字集合・旧字体対応表）を出典から生成する開発用ツール。

簡体字集合は Unicode の Unihan データベースから、旧字体対応表は常用漢字表
（平成22年内閣告示第2号）から生成する。生成物は data/ にコミットされるため、
検査時にネットワークへ出ることはない。
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zipfile import ZipFile


UNIHAN_URL = "https://www.unicode.org/Public/{version}/ucd/Unihan.zip"
JOYO_PAGE = "常用漢字一覧"
JOYO_API = "https://ja.wikipedia.org/w/api.php"
USER_AGENT = "check-japanese-text/0.2 (data generation)"

# 簡体字と判定する条件。
# kTraditionalVariant を持つ = 対応する繁体字がある = その字自身は簡体字。
# ただし日本語の新字体も同じ性質を持つため、日本の文字規格に採録されている字を除く。
# kIRG_JSource が JMJ-（文字情報基盤。戸籍統一文字などの異体字集合）だけの字は
# 日本語の通常表記には現れないため、採録されていない扱いとする。
SIMPLIFIED_PROPERTY = "kTraditionalVariant"
JAPANESE_SOURCE_PROPERTY = "kIRG_JSource"
JAPANESE_SOURCE_IGNORED_PREFIX = "JMJ"


def _load_unihan(payload: bytes) -> dict[str, dict[str, str]]:
    properties: dict[str, dict[str, str]] = {}
    with ZipFile(BytesIO(payload)) as archive:
        names = sorted(
            name
            for name in archive.namelist()
            if Path(name).name.startswith("Unihan") and name.endswith(".txt")
        )
        for name in names:
            for line in archive.read(name).decode("utf-8").splitlines():
                if not line or line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t", 2)
                if len(parts) != 3 or not parts[0].startswith("U+"):
                    continue
                character = chr(int(parts[0][2:], 16))
                properties.setdefault(character, {})[parts[1]] = parts[2]
    return properties


def extract_simplified(properties: dict[str, dict[str, str]]) -> set[str]:
    simplified: set[str] = set()
    for character, entry in properties.items():
        if SIMPLIFIED_PROPERTY not in entry:
            continue
        source = entry.get(JAPANESE_SOURCE_PROPERTY, "")
        if source and not source.startswith(JAPANESE_SOURCE_IGNORED_PREFIX):
            continue
        simplified.add(character)
    return simplified


def _fetch_joyo_wikitext() -> str:
    query = urlencode(
        {
            "action": "parse",
            "page": JOYO_PAGE,
            "prop": "wikitext",
            "format": "json",
            "formatversion": "2",
        }
    )
    request = Request(f"{JOYO_API}?{query}", headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:  # noqa: S310 - fixed official HTTPS origin
        return json.loads(response.read().decode("utf-8"))["parse"]["wikitext"]


_ROW_NUMBER = re.compile(r"^\s*(?:\{\{0[^}]*\}\}\s*)*\d+\s*$")
_WIKT_LINK = re.compile(r"\[\[wikt:([^\]|]+)[\]|]")


def extract_kyujitai(wikitext: str) -> list[tuple[str, str]]:
    """常用漢字一覧の表から (旧字体, 通用字体) の対を取り出す。"""
    pairs: list[tuple[str, str]] = []
    joyo: set[str] = set()
    for line in wikitext.splitlines():
        if not line.startswith("|"):
            continue
        cells = line[1:].split("||")
        if len(cells) < 5 or not _ROW_NUMBER.match(cells[0]):
            continue
        current = _WIKT_LINK.search(cells[1])
        old = _WIKT_LINK.search(cells[2])
        if not current or len(current.group(1)) != 1:
            continue
        joyo.add(current.group(1))
        if old and len(old.group(1)) == 1 and old.group(1) != current.group(1):
            pairs.append((old.group(1), current.group(1)))
    if len(joyo) != 2136:
        raise ValueError(f"常用漢字の総数が2136字と一致しない: {len(joyo)}字")
    conflicts = {old for old, _ in pairs} & joyo
    if conflicts:
        raise ValueError(f"旧字体が常用漢字と重複している: {''.join(sorted(conflicts))}")
    return sorted(pairs)


def render_simplified(characters: Iterable[str], version: str) -> str:
    header = (
        f"# Unicode {version} の Unihan データから生成。手で編集しない。\n"
        f"# 条件: {SIMPLIFIED_PROPERTY} を持ち、{JAPANESE_SOURCE_PROPERTY} が無いか"
        f" {JAPANESE_SOURCE_IGNORED_PREFIX}- のみ\n"
        "# 形式: code point<TAB>文字\n"
    )
    body = "".join(f"U+{ord(char):04X}\t{char}\n" for char in sorted(set(characters)))
    return header + body


def render_kyujitai(pairs: Iterable[tuple[str, str]]) -> str:
    header = (
        "# 常用漢字表（平成22年内閣告示第2号）の通用字体に対する旧字体。手で編集しない。\n"
        "# 出典: ja.wikipedia.org「常用漢字一覧」の旧字体欄"
        "（『新潮日本語漢字辞典』の旧字に基づく）\n"
        "# 形式: code point<TAB>旧字体<TAB>通用字体\n"
    )
    body = "".join(f"U+{ord(old):04X}\t{old}\t{new}\n" for old, new in pairs)
    return header + body


def generate(version: str, output_dir: Path) -> None:
    source = UNIHAN_URL.format(version=version)
    with urlopen(source) as response:  # noqa: S310 - fixed official HTTPS origin
        payload = response.read()
    properties = _load_unihan(payload)
    simplified = extract_simplified(properties)
    kyujitai = extract_kyujitai(_fetch_joyo_wikitext())

    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.joinpath("simplified_chars.txt").write_text(
        render_simplified(simplified, version), encoding="utf-8"
    )
    output_dir.joinpath("kyujitai_chars.txt").write_text(
        render_kyujitai(kyujitai), encoding="utf-8"
    )
    metadata = {
        "simplified": {
            "source": source,
            "sha256": sha256(payload).hexdigest(),
            "unicode_version": version,
            "character_count": len(simplified),
            "criteria": (
                f"{SIMPLIFIED_PROPERTY} present and "
                f"{JAPANESE_SOURCE_PROPERTY} absent or {JAPANESE_SOURCE_IGNORED_PREFIX}-only"
            ),
            "license": "Unicode-3.0",
        },
        "kyujitai": {
            "source": f"{JOYO_API}?action=parse&page={JOYO_PAGE}",
            "basis": "常用漢字表（平成22年内閣告示第2号）",
            "character_count": len(kyujitai),
            "license": "CC-BY-SA-4.0",
        },
    }
    output_dir.joinpath("data_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="同梱データを出典から生成する")
    parser.add_argument("--version", default="17.0.0")
    parser.add_argument("--output-dir", type=Path, default=Path("src/japanese_checker/data"))
    args = parser.parse_args()
    generate(args.version, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
