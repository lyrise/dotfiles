from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path
import sys
from typing import Sequence, TextIO

from japanese_checker.checker import CheckResult, Finding, check_text, load_words
from japanese_checker.fixer import FixEntry, apply_fixes, load_fix_words


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check-japanese-text",
        description="日本語テキストに混入した中国語を検出します。",
    )
    parser.add_argument(
        "file",
        nargs="*",
        default=["-"],
        help="UTF-8テキストファイル（複数指定可）。省略時または - は標準入力",
    )
    parser.add_argument(
        "--allow-words",
        action="append",
        default=[],
        metavar="PATH",
        help="許容語録ファイル（誤検出した正しい日本語を1語1行で登録）。複数指定可",
    )
    parser.add_argument(
        "--deny-words",
        action="append",
        default=[],
        metavar="PATH",
        help="検出語録ファイル（検出したい中国語句を1語1行で登録）。複数指定可",
    )
    parser.add_argument(
        "--fix-words",
        action="append",
        default=[],
        metavar="PATH",
        help="訂正語録ファイル（誤<TAB>正<TAB>理由。正が - なら報告専用）。複数指定可",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="訂正語録に従ってファイルを書き換え、そのうえで検出する。標準入力とは併用不可",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="結果をJSONで標準出力へ出力",
    )
    return parser


def _read_input(file_name: str) -> tuple[str, str]:
    if file_name == "-":
        return sys.stdin.buffer.read().decode("utf-8"), "<stdin>"
    path = Path(file_name)
    return path.read_bytes().decode("utf-8"), str(path)


def _finding_dict(finding: Finding) -> dict[str, object]:
    return {
        "start": finding.start,
        "end": finding.end,
        "line": finding.line,
        "column": finding.column,
        "text": finding.text,
        "detectors": list(finding.detectors),
        "reasons": list(finding.reasons),
    }


def _result_dict(
    source: str, result: CheckResult, applied: dict[str, int] | None = None
) -> dict[str, object]:
    payload: dict[str, object] = {
        "status": "contaminated" if result.contaminated else "clean",
        "source": source,
        "text_length": result.text_length,
        "chinese_specific_count": result.chinese_specific_count,
        "chinese_specific_ratio": result.chinese_specific_ratio,
        "suppressed_count": result.suppressed_count,
        "findings": [_finding_dict(finding) for finding in result.findings],
    }
    if applied is not None:
        payload["fixes_applied"] = applied
    return payload


def _print_human_summary(source: str, result: CheckResult, stream: TextIO) -> None:
    summary = (
        f"{source}: {len(result.findings)}件、"
        f"中国語固有文字 {result.chinese_specific_count}/{result.text_length} "
        f"({result.chinese_specific_ratio:.2%})"
    )
    if result.suppressed_count:
        summary += f"、許容語録で抑制 {result.suppressed_count}件"
    print(summary, file=stream)


def _print_human(
    source: str, result: CheckResult, stream: TextIO, applied: dict[str, int] | None = None
) -> None:
    if applied:
        detail = ", ".join(f"{label} x{count}" for label, count in applied.items())
        print(f"{source}: {sum(applied.values())}件訂正 ({detail})", file=stream)
    if not result.contaminated:
        print(f"{source}: OK: 中国語混入は検出されませんでした", file=stream)
        _print_human_summary(source, result, stream)
        return

    for finding in result.findings:
        detectors = ",".join(finding.detectors)
        reasons = " / ".join(finding.reasons)
        if "fix-flag" in finding.detectors:
            print(
                f"{source}:{finding.line}:{finding.column}: warn: "
                f"要確認 [fix-flag]: {finding.text!r} ({reasons})",
                file=stream,
            )
        else:
            print(
                f"{source}:{finding.line}:{finding.column}: error: "
                f"中国語混入を検出 [{detectors}]: {finding.text!r} ({reasons})",
                file=stream,
            )
    _print_human_summary(source, result, stream)


def _print_error(message: str, error_type: str, as_json: bool) -> None:
    if as_json:
        json.dump(
            {"status": "error", "error": {"type": error_type, "message": message}},
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
    else:
        print(f"check-japanese-text: error: {message}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.fix and not args.fix_words:
        _print_error("--fix には --fix-words の指定が必要です", "input_error", args.as_json)
        return 2
    try:
        allow_words: list[str] = []
        for path in args.allow_words:
            allow_words.extend(load_words(path))
        deny_words: list[str] = []
        for path in args.deny_words:
            deny_words.extend(load_words(path))
        fix_entries: tuple[FixEntry, ...] = ()
        for path in args.fix_words:
            fix_entries += load_fix_words(path)
        checked: list[tuple[str, CheckResult, dict[str, int]]] = []
        for name in args.file:
            text, source = _read_input(name)
            applied: dict[str, int] = {}
            if args.fix:
                if name == "-":
                    raise OSError("--fix は標準入力と併用できません")
                text, applied, flags = apply_fixes(text, fix_entries)
                Path(name).write_bytes(text.encode("utf-8"))
                result = check_text(text, allow_words, deny_words)
                if flags:
                    merged = tuple(
                        sorted(result.findings + flags, key=lambda finding: finding.start)
                    )
                    result = replace(result, findings=merged)
            else:
                result = check_text(text, allow_words, deny_words)
            checked.append((source, result, applied))
    except (OSError, UnicodeDecodeError, ValueError) as error:
        _print_error(str(error), "input_error", args.as_json)
        return 2
    except Exception as error:  # pragma: no cover - defensive CLI boundary
        _print_error(str(error), "internal_error", args.as_json)
        return 2

    if args.as_json:
        payloads = [
            _result_dict(source, result, applied if args.fix else None)
            for source, result, applied in checked
        ]
        payload: object = payloads[0] if len(payloads) == 1 else payloads
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for source, result, applied in checked:
            _print_human(source, result, sys.stderr, applied if args.fix else None)
    return 1 if any(result.contaminated for _, result, _ in checked) else 0


if __name__ == "__main__":
    raise SystemExit(main())
