# CLAUDE.md

## Overview
- 日本語で簡潔かつ丁寧に回答してください

## Plugins

### context7 (MCP)
- 外部ライブラリ・APIの情報取得は Context7 (MCP) で公式ドキュメントを参照し、最新の内容に基づいて対応する

### serena (MCP)
- 変数/シンボルの特定は `get_symbols_overview` や `find_symbol` を使い、参照先の確認は `find_referencing_symbols` を使う。名前が曖昧な場合は `search_for_pattern` を併用する
- メモリの参照/更新は `list_memories`/`read_memory`/`write_memory`/`delete_memory` を使う。メモリは `.serena/memories/` に保存されるため、必要に応じて調整する

## Git

### コミット
- `Co-Authored-By:` トレーラーは付けない
- `main` ブランチには直接コミットせず、必ずブランチを切ってからコミットする

## Tools

### Rust / Cargo
- `sccache` 経由で `cargo`、`rustc`、その他 Rust ツールチェーンのコマンドが失敗する場合、サンドボックスの問題なので、`RUSTC_WRAPPER` を外して再実行する (例: `env -u RUSTC_WRAPPER cargo`)
