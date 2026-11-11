from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


def run_cli(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "japanese_checker.cli", *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_parser_uses_public_command_name() -> None:
    from japanese_checker import cli

    assert cli._parser().prog == "check-japanese-text"


def test_clean_stdin_uses_exit_zero_and_stderr() -> None:
    completed = run_cli(input_text="これは日本語です。")

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert "OK" in completed.stderr


def test_contaminated_stdin_uses_exit_one() -> None:
    completed = run_cli(input_text="ここに这が混ざっています。")

    assert completed.returncode == 1
    assert "中国語混入を検出" in completed.stderr


def test_json_output_is_machine_readable() -> None:
    completed = run_cli("--json", input_text="ここに这があります。")

    assert completed.returncode == 1
    assert completed.stderr == ""
    payload = json.loads(completed.stdout)
    assert payload["status"] == "contaminated"
    assert payload["source"] == "<stdin>"
    assert payload["chinese_specific_count"] == 1
    assert payload["findings"][0]["line"] == 1


def test_reads_a_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "answer.txt"
    path.write_text("これは日本語です。", encoding="utf-8")

    completed = run_cli(str(path))

    assert completed.returncode == 0
    assert str(path) in completed.stderr


def test_missing_file_is_an_input_error() -> None:
    completed = run_cli("--json", "/does/not/exist")

    assert completed.returncode == 2
    payload = json.loads(completed.stdout)
    assert payload["status"] == "error"
    assert payload["error"]["type"] == "input_error"


def test_invalid_utf8_is_an_input_error(tmp_path: Path) -> None:
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"\xff")

    completed = run_cli("--json", str(path))

    assert completed.returncode == 2
    payload = json.loads(completed.stdout)
    assert payload["error"]["type"] == "input_error"


def test_allow_words_suppress_detection(tmp_path: Path) -> None:
    words = tmp_path / "allow_words.txt"
    words.write_text("# 許容語録\n这\t固有名詞\n", encoding="utf-8")

    completed = run_cli("--allow-words", str(words), input_text="ここに这があります。")

    assert completed.returncode == 0
    assert "OK" in completed.stderr
    assert "許容語録で抑制 1件" in completed.stderr


def test_deny_words_add_detection(tmp_path: Path) -> None:
    words = tmp_path / "deny_words.txt"
    words.write_text("# 検出語録\n水平\t見逃し対策\n", encoding="utf-8")

    completed = run_cli("--deny-words", str(words), input_text="この計画は水平に進む。")

    assert completed.returncode == 1
    assert "custom-deny" in completed.stderr


def test_multiple_files_are_reported_individually(tmp_path: Path) -> None:
    clean = tmp_path / "clean.txt"
    clean.write_text("これは日本語です。", encoding="utf-8")
    dirty = tmp_path / "dirty.txt"
    dirty.write_text("ここに这があります。", encoding="utf-8")

    completed = run_cli("--json", str(clean), str(dirty))

    assert completed.returncode == 1
    payloads = json.loads(completed.stdout)
    assert isinstance(payloads, list)
    assert [payload["source"] for payload in payloads] == [str(clean), str(dirty)]
    assert [payload["status"] for payload in payloads] == ["clean", "contaminated"]


def test_missing_word_file_is_an_input_error(tmp_path: Path) -> None:
    completed = run_cli("--json", "--allow-words", str(tmp_path / "missing.txt"))

    assert completed.returncode == 2
    payload = json.loads(completed.stdout)
    assert payload["error"]["type"] == "input_error"


def test_fix_rewrites_the_file_and_reports_applied_fixes(tmp_path: Path) -> None:
    path = tmp_path / "chapter.md"
    path.write_text("死后は靠近した。", encoding="utf-8")
    words = tmp_path / "fix_words.txt"
    words.write_text("死后\t死後\t簡体字\n靠近\t接近\t中国語語彙\n", encoding="utf-8")

    completed = run_cli("--fix", "--fix-words", str(words), str(path))

    assert completed.returncode == 0
    assert path.read_text(encoding="utf-8") == "死後は接近した。"
    assert "2件訂正" in completed.stderr
    assert "死后→死後 x1" in completed.stderr


def test_fix_flags_are_reported_without_touching_the_text(tmp_path: Path) -> None:
    path = tmp_path / "chapter.md"
    path.write_text("彼は逆袭を狙う。", encoding="utf-8")
    words = tmp_path / "fix_words.txt"
    words.write_text("逆袭\t-\t候補: 逆襲 / 下剋上\n", encoding="utf-8")

    completed = run_cli("--fix", "--fix-words", str(words), str(path))

    assert completed.returncode == 1
    assert path.read_text(encoding="utf-8") == "彼は逆袭を狙う。"
    assert "要確認 [fix-flag]" in completed.stderr


def test_fix_json_includes_applied_fixes(tmp_path: Path) -> None:
    path = tmp_path / "chapter.md"
    path.write_text("死后。", encoding="utf-8")
    words = tmp_path / "fix_words.txt"
    words.write_text("死后\t死後\t簡体字\n", encoding="utf-8")

    completed = run_cli(
        "--json", "--fix", "--fix-words", str(words), str(path)
    )

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert payload["status"] == "clean"
    assert payload["fixes_applied"] == {"死后→死後": 1}


def test_fix_is_opt_in_and_detection_only_by_default(tmp_path: Path) -> None:
    path = tmp_path / "chapter.md"
    path.write_text("袭は強い。", encoding="utf-8")
    words = tmp_path / "fix_words.txt"
    words.write_text("袭\t襲\t簡体字の残骸\n", encoding="utf-8")

    completed = run_cli("--fix-words", str(words), str(path))

    assert completed.returncode == 1
    assert path.read_text(encoding="utf-8") == "袭は強い。"


def test_fix_requires_fix_words(tmp_path: Path) -> None:
    path = tmp_path / "chapter.md"
    path.write_text("死后。", encoding="utf-8")

    completed = run_cli("--fix", str(path))

    assert completed.returncode == 2


def test_fix_cannot_read_from_stdin(tmp_path: Path) -> None:
    words = tmp_path / "fix_words.txt"
    words.write_text("死后\t死後\t簡体字\n", encoding="utf-8")

    completed = run_cli("--fix", "--fix-words", str(words), input_text="死后。")

    assert completed.returncode == 2


def test_fix_preserves_line_endings(tmp_path: Path) -> None:
    path = tmp_path / "chapter.md"
    path.write_bytes("死后は笑った。\r\nまだ死后。\r\n".encode("utf-8"))
    words = tmp_path / "fix_words.txt"
    words.write_text("死后\t死後\t簡体字\n", encoding="utf-8")

    completed = run_cli("--fix", "--fix-words", str(words), str(path))

    assert completed.returncode == 0
    assert path.read_bytes() == "死後は笑った。\r\nまだ死後。\r\n".encode("utf-8")
