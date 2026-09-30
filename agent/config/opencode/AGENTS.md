# AGENTS.md

## Overview
- 日本語で簡潔かつ丁寧に回答してください

## Plugins

### context7 (MCP)
- 外部ライブラリ・APIの情報取得は Context7 (MCP) で公式ドキュメントを参照し、最新の内容に基づいて対応する

### serena (MCP)
- 変数/シンボルの特定は `get_symbols_overview` や `find_symbol` を使い、参照先の確認は `find_referencing_symbols` を使う。名前が曖昧な場合は `search_for_pattern` を併用する

### memory (SKILL)
- 関連する知識・個人文脈が必要なときは `memory-knowledges` スキル、過去の調査記録が必要なときは `memory-records` スキルに従い、環境変数 `AGENT_MEMORY_DIR` が指すディレクトリを優先して参照する
- `AGENT_MEMORY_DIR` への保存は明示依頼時だけ行う。Codex・Claude・Serena の Memory は参照・保存に使わない
- `AGENT_MEMORY_DIR` が未設定、または指すディレクトリが存在しない場合はその旨を報告し、別の Memory に切り替えない

### playwright-cli (SKILL)
- Web UI や localhost のブラウザ検証、DOM 操作、console/network 確認が必要な場合に使用する
- 操作対象は snapshot の element ref で特定し、必要に応じて `eval`、`console`、`network` で状態を確認する
- screenshot はレイアウトや表示崩れの確認など、視覚的な証拠が必要な場合に限定して使用する

## Agents
- チェックは `verifier` サブエージェントに任せ、`pass` / `changes-required` の判定を受け取る

## Rust
- サンドボックス内で Cargo が Rust コンパイラを起動し得るコマンド（`build`、`check`、`test`、`clippy`、`run`、`doc` など）を実行するときは、最初から `RUSTC_WRAPPER= cargo ...` として sccache を無効化する
- `fmt`、`metadata`、`clean` など Rust コンパイラを起動しない Cargo コマンドは対象外とする

## Git

### コミット
- コミットメッセージの末尾に、コミットを作成したエージェント自身のモデルを示す `Co-Authored-By:` トレーラーを必ず 1 行付ける
  - 形式: `Co-Authored-By: <モデル名> <noreply@<プロバイダーのドメイン>>`（例: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`）
  - ハーネスがトレーラーの値を指定している場合は、その値に従う
  - モデル名やプロバイダーを確認できない場合は推測せず、分からない部分をツール名で補う（例: `Co-Authored-By: opencode <noreply@opencode.ai>`）
