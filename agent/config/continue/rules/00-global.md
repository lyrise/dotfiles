---
name: Global
alwaysApply: true
---

# Global

## Overview
- 日本語で簡潔かつ丁寧に回答してください
- 不明点があり、作業の正確性に影響する場合は、必要に応じて質問してください

## Skills
- 利用可能な skill が作業内容に該当する場合は、着手前に `read_skill` でその内容を読み、記載された手順に従う
- skill は `~/.continue/skills`、`.continue/skills`、`.claude/skills` から読み込まれる

### obsidian (MCP)
- 関連する知識・個人文脈が必要なときは `obsidian-knowledges` スキル、過去の調査記録が必要なときは `obsidian-records` スキルに従い、Obsidian vault の `share/` を優先して参照する
- Obsidian への保存は明示依頼時だけ行う。Codex・Claude・Serena の Memory は参照・保存に使わない
- Obsidian MCP が使えない場合はその旨を報告し、別の Memory に切り替えない

### playwright-cli (SKILL)
- Web UI や localhost のブラウザ検証、DOM 操作、console/network 確認が必要な場合に使用する
- 操作対象は snapshot の element ref で特定し、必要に応じて `eval`、`console`、`network` で状態を確認する
- screenshot はレイアウトや表示崩れの確認など、視覚的な証拠が必要な場合に限定して使用する

## Rust
- サンドボックス内で Cargo が Rust コンパイラを起動し得るコマンド（`build`、`check`、`test`、`clippy`、`run`、`doc` など）を実行するときは、最初から `RUSTC_WRAPPER= cargo ...` として sccache を無効化する
- `fmt`、`metadata`、`clean` など Rust コンパイラを起動しない Cargo コマンドは対象外とする

## Git

### コミット
- コミットメッセージの末尾に、コミットを作成したエージェント自身のモデルを示す `Co-Authored-By:` トレーラーを必ず 1 行付ける
  - 形式: `Co-Authored-By: <モデル名> <noreply@<プロバイダーのドメイン>>`（例: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`）
  - ハーネスがトレーラーの値を指定している場合は、その値に従う
  - モデル名やプロバイダーを確認できない場合は推測せず、分からない部分をツール名で補う（例: `Co-Authored-By: Continue <noreply@continue.dev>`）
