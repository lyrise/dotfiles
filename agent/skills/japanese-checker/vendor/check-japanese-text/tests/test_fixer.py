from __future__ import annotations

import pytest

from japanese_checker.fixer import FixEntry, apply_fixes, load_fix_words


def _entries(*rows: tuple[str, str, str]) -> tuple[FixEntry, ...]:
    return tuple(FixEntry(wrong=w, right=r, reason=reason) for w, r, reason in rows)


def test_apply_fixes_replaces_and_counts() -> None:
    entries = _entries(("死后", "死後", "簡体字"), ("袭", "襲", "簡体字"))

    fixed, applied, flags = apply_fixes("死后は袭を避けた。死后。", entries)

    assert fixed == "死後は襲を避けた。死後。"
    assert applied == {"死后→死後": 2, "袭→襲": 1}
    assert flags == ()


def test_flag_only_entries_report_without_rewriting() -> None:
    entries = _entries(("逆袭", "-", "候補: 逆襲 / 下剋上"))

    fixed, applied, flags = apply_fixes("彼は逆袭を狙う。", entries)

    assert fixed == "彼は逆袭を狙う。"
    assert applied == {}
    assert len(flags) == 1
    assert flags[0].text == "逆袭"
    assert flags[0].detectors == ("fix-flag",)
    assert flags[0].line == 1


def test_flag_positions_are_taken_from_the_text_before_fixing() -> None:
    """報告専用の発見は訂正前の本文に対して探す。置換で消えた語も報告する。"""
    entries = _entries(("袭", "襲", "簡体字"), ("逆袭", "-", "候補複数"))

    fixed, applied, flags = apply_fixes("逆袭", entries)

    assert fixed == "逆襲"
    assert applied == {"袭→襲": 1}
    assert len(flags) == 1
    assert flags[0].text == "逆袭"


def test_flag_rows_carry_the_reason() -> None:
    entries = _entries(("是存在", "-", "中国語の判断詞"))

    _, _, flags = apply_fixes("それは是存在する。", entries)

    assert flags[0].reasons == ("中国語の判断詞",)


def test_apply_fixes_on_empty_text() -> None:
    fixed, applied, flags = apply_fixes("", _entries(("死后", "死後", "")))

    assert fixed == ""
    assert applied == {}
    assert flags == ()


def test_load_fix_words_parses_rows_comments_and_flags(tmp_path) -> None:
    path = tmp_path / "fix_words.txt"
    path.write_text(
        "# コメント\n\n死后\t死後\t簡体字\n逆袭\t-\t候補複数\n",
        encoding="utf-8",
    )

    entries = load_fix_words(path)

    assert entries == (
        FixEntry(wrong="死后", right="死後", reason="簡体字"),
        FixEntry(wrong="逆袭", right="-", reason="候補複数"),
    )


@pytest.mark.parametrize("line", ["語のみ", "\t正だけ", "誤\t\t理由なし"])
def test_load_fix_words_rejects_malformed_rows(tmp_path, line: str) -> None:
    path = tmp_path / "fix_words.txt"
    path.write_text(line + "\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_fix_words(path)
