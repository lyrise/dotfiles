# CLAUDE.md

## Overview
- 日本語で簡潔かつ丁寧に回答してください
- 不明点があり、作業の正確性に影響する場合は、必要に応じて質問してください

## Plugins

### context7 (MCP)
- 外部ライブラリ・APIの情報取得は Context7 (MCP) で公式ドキュメントを参照し、最新の内容に基づいて対応する

### serena (MCP)
- 変数/シンボルの特定は `get_symbols_overview` や `find_symbol` を使い、参照先の確認は `find_referencing_symbols` を使う。名前が曖昧な場合は `search_for_pattern` を併用する
- メモリの参照/更新は `list_memories`/`read_memory`/`write_memory`/`delete_memory` を使う。メモリは `.serena/memories/` に保存されるため、必要に応じて調整する

### playwright-cli (SKILL)
- Web UI や localhost のブラウザ検証、DOM 操作、console/network 確認が必要な場合に使用する
- 操作対象は snapshot の element ref で特定し、必要に応じて `eval`、`console`、`network` で状態を確認する
- screenshot はレイアウトや表示崩れの確認など、視覚的な証拠が必要な場合に限定して使用する

## Rust
- サンドボックス内で Cargo が Rust コンパイラを起動し得るコマンド（`build`、`check`、`test`、`clippy`、`run`、`doc` など）を実行するときは、最初から `RUSTC_WRAPPER= cargo ...` として sccache を無効化する
- `fmt`、`metadata`、`clean` など Rust コンパイラを起動しない Cargo コマンドは対象外とする

## Git

### コミット
- `Co-Authored-By:` トレーラーは付けない

### PR作成
- PR本文の末尾に `🤖 Generated with [Claude Code](https://claude.com/claude-code)` などの生成元表記は付けない
