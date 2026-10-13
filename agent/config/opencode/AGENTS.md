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
- チェック検証は、Paseo MCP が使える場合、本体と異なるモデルファミリーの検証役を Paseo で作って行う
  - `list_profiles` で `verifier-` で始まるプロファイルを確認し、notes の family が本体のモデルと異なるものを priority の小さい順に選ぶ。ファミリーは CLI ではなくモデルで判定する
  - プロファイルの provider/model と `modeId` を `create_agent` に写し、本体と同じワークスペースで作る。initialPrompt には `agents/verifier.md` の規範本文と検証対象を転記し、ファイルを変更しないよう明示する
  - `pass` / `changes-required` の判定を受け取るまで待つ。検証役からの権限要求はすべて拒否し、実行できなかった確認は未検証の領域として報告させる。判定を受け取ったら `archive_agent` で整理する
  - 作成や実行に失敗した場合は次のプロファイルを試す
- Paseo MCP が使えない場合、または使えるプロファイルがない場合は `verifier` サブエージェントに任せ、本体と同系モデルでの検証になった旨を判定とともに報告する
- どちらの手段でも、検証役による作業ツリーの改変を検知する
  - 検証の前後で、`AGENT_TEMP_DIR` 内の新しい一時インデックスを `GIT_INDEX_FILE` に指定して `git add -A` と `git write-tree` を実行し、得たツリーと `git rev-parse HEAD` を比べる
  - 違いがあれば判定を採用せず、検証前後のツリーの差分（`git diff <前> <後>`）をユーザーに示して指示を待つ。自動では戻さない
  - 検証対象が git 管理外の場合は、改変を検知できなかった旨を判定とともに報告する
- 上記以外のサブエージェント・paseo でのエージェント作成は極力行わない。探索・調査・実装も本体で直接ツールを実行して対応する（サブエージェントはコンテキストを複製しトークン消費が大きいため）。ユーザーが明示的に指定した場合はその限りではない

## 一時ディレクトリ
- 自分で作る一時ファイル・一時ディレクトリ（mktemp、スクラッチ、検証の中間物など）は、環境変数 `AGENT_TEMP_DIR` が指すディレクトリの中に置く。ツールが内部で使うキャッシュ等は対象外
- `AGENT_TEMP_DIR` が未設定のときはその旨を報告して通常どおり `/tmp` を使う。指すディレクトリが存在しないときは `mkdir -p` してから使う

## Rust
- サンドボックス内で Cargo が Rust コンパイラを起動し得るコマンド（`build`、`check`、`test`、`clippy`、`run`、`doc` など）を実行するときは、最初から `RUSTC_WRAPPER= cargo ...` として sccache を無効化する
- `fmt`、`metadata`、`clean` など Rust コンパイラを起動しない Cargo コマンドは対象外とする

## Git

### コミット
- コミットメッセージの末尾に、コミットを作成したエージェント自身のモデルを示す `Co-Authored-By:` トレーラーを必ず 1 行付ける
  - 形式: `Co-Authored-By: <モデル名> <noreply@<プロバイダーのドメイン>>`（例: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`）
  - ハーネスがトレーラーの値を指定している場合は、その値に従う
  - モデル名やプロバイダーを確認できない場合は推測せず、分からない部分をツール名で補う（例: `Co-Authored-By: opencode <noreply@opencode.ai>`）
