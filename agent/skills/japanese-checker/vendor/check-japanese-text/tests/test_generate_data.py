from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

import pytest

from tools.generate_data import (
    _load_unihan,
    extract_kyujitai,
    extract_simplified,
    render_kyujitai,
    render_simplified,
)


def _unihan_zip(lines: list[str]) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr("Unihan_Variants.txt", "\n".join(lines))
    return buffer.getvalue()


def test_extract_simplified_keeps_characters_outside_japanese_standards() -> None:
    payload = _unihan_zip(
        [
            "# comment",
            "U+4E1C\tkTraditionalVariant\tU+6771",
            "U+9759\tkTraditionalVariant\tU+975C",
            "U+9759\tkIRG_JSource\tJ0-4048",
            "U+4E00\tkMandarin\tyi1",
        ]
    )

    assert extract_simplified(_load_unihan(payload)) == {"东"}


def test_extract_simplified_ignores_moji_joho_only_sources() -> None:
    """JMJ- だけの字は日本語の通常表記に現れないため採録扱いにしない。"""
    payload = _unihan_zip(
        [
            "U+8FD9\tkTraditionalVariant\tU+9019",
            "U+8FD9\tkIRG_JSource\tJMJ-025811",
        ]
    )

    assert extract_simplified(_load_unihan(payload)) == {"这"}


def _joyo_row(number: int, current: str, old: str | None) -> str:
    old_cell = f' style="x" | [[wikt:{old}|{old}]]' if old else ""
    return (
        f"| {{{{0}}}}{number} || style=\"x\" | [[wikt:{current}|{current}]] ||{old_cell}"
        ' || style="x" | [[部首|部]] || 7 || S || || || ヨミ'
    )


def test_extract_kyujitai_pairs_old_forms_with_current_forms() -> None:
    # 亜（U+4E9C）と重ならない範囲から、表の総数に足りる字を埋める。
    filler = [chr(code) for code in range(0x5000, 0x5000 + 2135)]
    rows = [_joyo_row(1, "亜", "亞")]
    rows += [_joyo_row(number, char, None) for number, char in enumerate(filler, start=2)]
    wikitext = "\n".join(rows)

    assert extract_kyujitai(wikitext) == [("亞", "亜")]


def test_extract_kyujitai_rejects_a_table_of_the_wrong_size() -> None:
    with pytest.raises(ValueError, match="2136字"):
        extract_kyujitai(_joyo_row(1, "亜", "亞"))


def test_render_simplified_emits_sorted_code_points_with_a_header() -> None:
    rendered = render_simplified({"东", "这"}, "17.0.0")

    assert rendered.startswith("# Unicode 17.0.0 の Unihan データから生成")
    assert rendered.splitlines()[-2:] == ["U+4E1C\t东", "U+8FD9\t这"]


def test_render_kyujitai_keeps_the_current_form_alongside_the_old_one() -> None:
    rendered = render_kyujitai([("亞", "亜")])

    assert rendered.splitlines()[-1] == "U+4E9E\t亞\t亜"
