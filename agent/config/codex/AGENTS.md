# AGENTS.md

## Overview
- 日本語で簡潔かつ丁寧に回答してください

## Plugins

### context7 (MCP)
- 外部ライブラリ・APIの情報取得は Context7 (MCP) で公式ドキュメントを参照し、最新の内容に基づいて対応する

### serena (MCP)
- 変数/シンボルの特定は `get_symbols_overview` や `find_symbol` を使い、参照先の確認は `find_referencing_symbols` を使う。名前が曖昧な場合は `search_for_pattern` を併用する
- メモリの参照/更新は `list_memories`/`read_memory`/`write_memory`/`delete_memory` を使う。メモリは `.serena/memories/` に保存されるため、必要に応じて調整する

### brave-search (MCP)
- 外部情報の検索はBrave Searchで行う。検索クエリは英語で行う。

### computer-use (MCP)
- macOS アプリの操作、GUI 状態の確認、目視前提の検証が必要な場合に使用する
- 操作前に `get_app_state` で対象アプリの状態を確認し、可能な限り座標クリックより accessibility element を優先する
- テキスト入力やボタン操作は、現在フォーカスと画面状態を確認してから最小限に行う

### xcodebuildmcp (MCP)
- iOS / Simulator の build、run、test、debug は xcodebuildmcp を優先して使用する
- 最初の build/run/test 前に `session_show_defaults` で project、scheme、destination などの既定値を確認する
- 必要に応じて `list_sims`、`build_sim`、`build_run_sim`、`test_sim`、`screenshot` を使い分け、結果と未検証範囲を明示する

### playwright-cli (SKILL)
- Web UI や localhost のブラウザ検証、DOM 操作、console/network 確認が必要な場合に使用する
- 操作対象は snapshot の element ref で特定し、必要に応じて `eval`、`console`、`network` で状態を確認する
- screenshot はレイアウトや表示崩れの確認など、視覚的な証拠が必要な場合に限定して使用する

### codex_apps (MCP)
- GitHub、Google Drive、Slack などの app/connector 上の情報が必要な場合は codex_apps を優先して参照する
- PR、Issue、レビューコメント、外部サービス上のファイルなどは、ローカル checkout より connector 側を source of truth として扱う
- 作成・更新・削除などの変更系操作では、対象、変更内容、意図を明確にしてから実行する
