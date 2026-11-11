from __future__ import annotations

import pytest

from japanese_checker.checker import check_text


@pytest.mark.parametrize(
    ("text", "detector"),
    [
        ("ここに这が混ざっています。", "simplified"),
        ("中国企業の腾讯について説明します。", "simplified"),
        ("彼女は獻身的に尽くした。", "kyujitai"),
        ("靜かな時間が流れる。", "kyujitai"),
        ("気持ちが傳わる。", "kyujitai"),
        ("影が靠近してくる気配があった。", "unknown-word"),
        ("彼女は言った。這個是我的書。", "unknown-word"),
        ("我在日本生活。", "chinese-sentence"),
        ("彼女は言った。我明日去学校。", "chinese-sentence"),
    ],
)
def test_detects_contamination_with_expected_detector(text: str, detector: str) -> None:
    result = check_text(text)

    assert result.contaminated
    assert any(detector in finding.detectors for finding in result.findings)


@pytest.mark.parametrize(
    "text",
    [
        "これは日本語の文章です。新しい機能を確認します。",
        "妙蓮は静かに息を吐き、庭先の桜を見上げた。",
        "第三章　封印解除　妖魔討伐戦記",
        "三号室の一区切りを守る者だ。",
        "戦闘区域の黄金を回収する。",
        "彼は電光石火の勢いで疾風迅雷の一撃を放った。",
        "絶体絶命。",
        "OpenAI APIを利用して結果を生成します。",
        "This is an English sentence.",
        "",
    ],
)
def test_accepts_japanese_text(text: str) -> None:
    assert not check_text(text).contaminated


def test_ignores_headings_and_list_items_in_sentence_detection() -> None:
    """見出しと箇条書きは文ではないため、中国語文の判定から外す。"""
    text = "# 第三章 封印解除\n- **種族**: 人類\n| 用語 | 説明 |\n"

    assert not check_text(text).contaminated


def test_allows_only_the_occurrence_covered_by_an_allow_word() -> None:
    """許容語は本文での出現位置で効く。同じ字が別の場所に出れば検出は残る。"""
    result = check_text("东京大学に通う。东の空。", allow_words=("东京大学",))

    assert [finding.text for finding in result.findings] == ["东"]
    assert result.findings[0].line == 1
    assert result.suppressed_count == 1


def test_ignores_titles_that_do_not_end_in_a_full_stop() -> None:
    """句点で終わらない断片は題名であって文ではない。"""
    assert not check_text("第三章　封印解除　妖魔討伐戦記").contaminated


def test_allow_word_does_not_leak_into_a_longer_finding() -> None:
    """1字の許容語が、それを含むだけの長い検出区間を消してはならない。"""
    result = check_text("彼女は言った。我明日去学校。", allow_words=("学",))

    assert result.contaminated


def test_deny_words_detect_phrases_the_detectors_miss() -> None:
    text = "この術は可以使用の状態にある。"

    assert not check_text(text).contaminated
    result = check_text(text, deny_words=("可以使用",))
    assert [finding.detectors for finding in result.findings] == [("custom-deny",)]


def test_reports_position_of_each_finding() -> None:
    result = check_text("一行目は日本語。\nここに这が混ざる。")

    (finding,) = result.findings
    assert (finding.text, finding.line, finding.column) == ("这", 2, 4)


def test_numbers_are_not_reported_as_unknown_words() -> None:
    """数詞は未知語になりやすいが日本語として正しい。"""
    assert not check_text("第三章の一六八ページ。").contaminated


def test_counts_every_specific_character_occurrence() -> None:
    result = check_text("あ这这")

    assert result.text_length == 3
    assert result.chinese_specific_count == 2
    assert result.chinese_specific_ratio == pytest.approx(2 / 3)
