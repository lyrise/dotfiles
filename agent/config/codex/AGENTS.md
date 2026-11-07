# AGENTS.md

## Overview
- 日本語で丁寧に回答してください。結論を先に示し、判断に影響する前提・代替案・懸念は省略しないでください
- 調査や設計の相談では、依頼された範囲の周辺（影響範囲、既存の設計、見落としやすい観点）にも目を向け、気づいたことは報告してください
- 不明点があり、作業の正確性に影響する場合は、必要に応じて質問してください

## Plugins

### context7 (MCP)
- 外部ライブラリ・APIの情報取得は Context7 (MCP) で公式ドキュメントを参照し、最新の内容に基づいて対応する

### memory (SKILL)
- 関連する知識・個人文脈が必要なときは `memory-knowledge` スキル、過去の調査記録が必要なときは `memory-records` スキルに従い、環境変数 `AGENT_MEMORY_DIR` が指すディレクトリを優先して参照する
- `AGENT_MEMORY_DIR` への保存は明示依頼時だけ行う。Codex・Claude の Memory は参照・保存に使わない
- `AGENT_MEMORY_DIR` が未設定、または指すディレクトリが存在しない場合はその旨を報告し、別の Memory に切り替えない

### playwright-cli (SKILL)
- Web UI や localhost のブラウザ検証、DOM 操作、console/network 確認が必要な場合に使用する
- 操作対象は snapshot の element ref で特定し、必要に応じて `eval`、`console`、`network` で状態を確認する
- screenshot はレイアウトや表示崩れの確認など、視覚的な証拠が必要な場合に限定して使用する

## Agents
- チェック検証は、Paseo MCP が使える場合、本体と異なるモデルファミリーの検証役を Paseo で作って行う
  - `list_profiles` で `verifier-` で始まるプロファイルを確認し、notes の family が本体のモデルと異なるものを priority の小さい順に選ぶ。ファミリーは CLI ではなくモデルで判定する
  - プロファイルの provider/model と `modeId` を `create_agent` に写し、本体と同じワークスペースで作る。initialPrompt には `agents/verifier.toml` の規範本文と検証対象を転記し、ファイルを変更しないよう明示する
  - `notifyOnFinish` を有効にして検証役を作成・送信し、権限要求と完了の通知を受け取る。通知が届かない場合は `get_agent_status` で状態を確認する
  - 権限要求の通知を受けたら、`list_pending_permissions` で検証役のリクエストだけを確認し、`respond_to_permission` で 1 回限りの承認または拒否を返す
  - 作成や実行に失敗した場合は次のプロファイルを試す
- Paseo MCP が使えない場合、または使えるプロファイルがない場合は `verifier` サブエージェントに任せ、本体と同系モデルでの検証になった旨を判定とともに報告する
- 検証役への権限承認は、Paseo 経路では `respond_to_permission`、サブエージェント経路ではユーザー承認を使い、どちらも次の基準に従う
  - 承認する: 読み取り専用のファイル閲覧・検索、git の読み取り (`status` / `diff` / `log` / `show` / `blame` / `grep` / `ls-files`)、テキスト処理 (`sort` / `uniq` / `diff` / `jq` など)、`gh` の読み取り (`pr view` / `pr diff` / `issue view`)、依頼で明示されたパスや `AGENT_MEMORY_DIR` の読み取り、通常の http(s) ドキュメント取得
  - 拒否する: 編集・書き込み・削除・移動、ビルド・テスト・パッケージ導入、git の書き込み、外部送信・公開、権限昇格・システム操作、秘密ファイル (`.env` / `.ssh` / `.aws` / 認証情報)、永続化・自己改変、クラウド・DB・コンテナの更新、MCP の更新系
  - 判断に迷う場合はユーザーに確認し、応答が得られない場合は拒否する。拒否理由を検証役に伝え、その確認は未検証の領域として報告させる
  - サブエージェント経路でユーザーが承認できない場合も、拒否対象は承認の有無にかかわらず拒否し、権限が必要な確認は未検証の領域として報告させる
- 検証役の応答が `STATUS: needs-input` なら、事実 (ファイル、差分、実行済み検証の結果など) は本体が回答し、意図・受容判断・権限はユーザーに確認する。Paseo 経路では `send_agent_prompt` で同じ検証役に送って再開し、サブエージェント経路では回答を含めて再実行する。この往復は最大 2 回
- 2 往復後も `STATUS: needs-input` なら、今ある情報で最終判定を出すよう指示する。それでも `needs-input` なら打ち切り、未解決の確認項目と未検証領域を報告する
- `STATUS: pass` / `STATUS: changes-required` が最終判定。`STATUS: changes-required` に確認項目が併記されていれば、回答と修正を行って再検証する。Paseo 経路では判定を受け取ったら `archive_agent` で整理する
- `STATUS: changes-required` の修正・再検証は最大 2 往復。`needs-input` の往復とは別に数える
- 検証役の応答に `STATUS:` 行がない場合は状態を再確認させ、それでも得られなければ判定を採用しない
- どちらの手段でも、検証役による作業ツリーの改変を検知する
  - 検証の前後で、`AGENT_TEMP_DIR` 内の新しい一時インデックスを `GIT_INDEX_FILE` に指定して `git add -A` と `git write-tree` を実行し、得たツリーと `git rev-parse HEAD` を比べる
  - 違いがあれば判定を採用せず、検証前後のツリーの差分（`git diff <前> <後>`）をユーザーに示して指示を待つ。自動では戻さない
  - 検証対象が git 管理外の場合は、改変を検知できなかった旨を判定とともに報告する
- 最終報告に、検証役への質問と回答、承認・拒否した権限と理由、未検証領域を含める
- 上記以外のサブエージェント・paseo でのエージェント作成は極力行わない。探索・調査・実装も本体で直接ツールを実行して対応する。ユーザーが明示的に指定した場合はその限りではない

## 一時ディレクトリ
- 自分で作る一時ファイル・一時ディレクトリ（mktemp、スクラッチ、検証の中間物など）は、環境変数 `AGENT_TEMP_DIR` が指すディレクトリの中に置く。ツールが内部で使うキャッシュ等は対象外
- `AGENT_TEMP_DIR` が未設定のときはその旨を報告して通常どおり `/tmp` を使う。指すディレクトリが存在しないときは `mkdir -p` してから使う

## Rust
- サンドボックス内で Cargo が Rust コンパイラを起動し得るコマンド（`build`、`check`、`test`、`clippy`、`run`、`doc` など）を実行するときは、最初から `RUSTC_WRAPPER= cargo ...` として sccache を無効化する
- `fmt`、`metadata`、`clean` など Rust コンパイラを起動しない Cargo コマンドは対象外とする

## Git

### GitHub
- GitHub の PR、Issue、レビュー、Actions の操作と参照は `gh` CLI を第一選択とする
- `gh` が sandbox やネットワーク制限で失敗した可能性がある場合は、認証切れと断定せず、同じコマンドを必要な権限付きで再実行する

### コミット
- コミットメッセージの末尾に、コミットを作成したエージェント自身のモデルを示す `Co-Authored-By:` トレーラーを必ず 1 行付ける
  - 形式: `Co-Authored-By: <モデル名> <noreply@<プロバイダーのドメイン>>`（例: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`）
  - ハーネスがトレーラーの値を指定している場合は、その値に従う
  - モデル名やプロバイダーを確認できない場合は推測せず、分からない部分をツール名で補う（例: `Co-Authored-By: Codex <noreply@openai.com>`）
