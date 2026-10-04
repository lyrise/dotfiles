---
name: paseo-resume
description: Paseo でエージェントがレート制限・使用制限(usage limit / rate limit / limit reset)で停止した際、リセット時刻の5分後に自動で再開させる手順。対象エージェントの状態と承認待ちの確認、重複送信の防止、単発スケジュールの作成と検証を扱う。「レート制限で止まった」「リセットされたら再開して」「23:10 に制限リセット」「limit reset at 23:10」「使用制限がかかったから後で続けて」など、Paseo エージェントの制限解除後の再開・遅延再開を頼まれたときに必ず使用する。
---

# Paseo エージェントのレート制限リセット後の遅延再開

Paseo のエージェントがレート制限で停止したとき、リセット時刻まで人間が再 prompt し続けるのは非生産的である。この手順では、リセット時刻の5分後に単発で発火するスケジュールを作成し、ヘルパーエージェント経由で対象の既存会話を継続させる。Paseo ツールの詳細な仕様は paseo スキルを参照すること。

## 重要な前提(なぜこの手順なのか)

- `create_heartbeat` は使えない。heartbeat は呼び出し元自身を再 prompt する仕組みで、対象エージェントを指定する引数が存在しない。agent-scoped session が前提になる。
- `create_schedule` は新しいエージェント(ヘルパー)を起動する。既存会話の継続は、ヘルパーが `paseo_send_agent_prompt` に対象の agent ID を送ることで実現する。`send_agent_prompt` は対象の既存 conversation を継続できる。
- agent-scoped なスケジュール作成では、caller の mode や provider 設定・feature を継承する場合がある。承認モードと plan mode を別々に確認する。承認モードを変更するだけで plan mode も無効になるとは限らない。
- 自動審査（OpenCode では一律承認）の対象はヘルパー自身の MCP 呼び出しである。対象エージェントの承認待ちを承認することとは別であり、対象の権限承認は禁止する。自動審査は再開成功を保証せず、拒否や追加の承認確認があれば送信を中止する。

## プロバイダー別のヘルパー設定

ヘルパーの provider/model を特定し、`paseo_inspect_provider` にその provider、対象の `cwd`、使用する model を `settings.model` で渡す。対象エージェントとヘルパーの provider が同じとは限らない。返された modes/features と MCP の現在の引数仕様を確認してから、該当する provider の節に従う。

全 provider に共通する事項:

- 確認時点のスケジュール MCP では、`create_schedule` に mode 引数がなく、`update_schedule` の `mode` で変更する。provider options や feature を変更する引数はない。未公開の `settings`、`providerOptions`、`featureValues` などを推測して渡さない。追加引数を受け付けても、更新処理が無視する場合がある。
- `mode` は各節の値を明示する。保存後は、スケジュールの new-agent 起動設定に対応する mode ID（例: `target.config.modeId`）が保存されたことを確認する。
- 更新経路がない設定は、継承される設定と既定値から各節の条件を満たすと確認できる場合だけ利用する。model 未指定の照会や空の features 一覧だけで、継承値を判断しない。
- 必要な mode・feature を MCP 経由で設定・検証できない場合、または provider が無効な場合は作成を中止する。CLI、SDK、グローバル設定、caller や対象エージェントの設定の変更で補わない。

### Codex (`codex`)

- mode: `auto-review`。`auto` は Default Permissions であり、自動審査モードではない。
- 中止条件: `auto-review` が未提供・利用不可の場合。`full-access` に切り替えない。
- 中止条件: `plan_mode` feature が有効な場合。現在の MCP では無効化できないため、継承値が無効だと確認できたときだけ進める。MCP が feature 更新をサポートした場合は無効に設定する。
- 検証項目: mode が `auto-review` であり、`plan_mode` が無効であること。

### Claude Code (`claude`)

- mode: `auto`。モデルの classifier が権限要求を自動審査する。`plan` を継承した場合も `auto` に変更する。Codex の `auto-review` や `plan_mode` feature を流用しない。
- 中止条件: `auto` が未提供・利用不可の場合。`bypassPermissions` に切り替えない。
- 中止条件: 明示的な ask rule やユーザー操作を必須とする MCP ツールなどで承認確認が残り、必要な4ツールを無人で実行できない場合。
- 検証項目: mode が `auto` であり、`plan` ではないこと。

### OpenCode (`opencode`)

- mode: `build`（一覧に存在する場合）。mode は使用する agent の選択であり、自動審査の指定ではない。
- 権限: 限定しない。OpenCode には自動審査の仕組みがないため、Codex・Claude Code と異なり `auto_accept` による一律承認を例外として許容する。承認待ちでヘルパーが停止することを避けるため、`auto_accept` は常に `true` とする。
- 中止条件: 継承した `auto_accept` が `true` だと確認できない場合（`false` または不明）。現在の MCP では設定できないため、継承値で判断する。MCP が feature 更新をサポートした場合は `true` を明示的に設定する。
- 検証項目: mode が `build` であり、`auto_accept` が `true` であること。
- 安全策は prompt による禁止だけになる。実行時の制約はないことを最終報告で明示する。

仕様の根拠: [Codex Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)、[Claude Code permission modes](https://code.claude.com/docs/en/permission-modes)、[OpenCode agents](https://opencode.ai/docs/agents/)、[Paseo provider options](https://github.com/getpaseo/paseo/blob/main/public-docs/sdk/provider-options.md)。実行時は接続先 Paseo のツール仕様・provider 情報を優先する。

## 手順

### 0. Paseo MCP の確認

- 最初に Paseo MCP のツールが見えることを確認する。見えない場合は、その旨をユーザーに報告して中断する。
- MCP が見えない場合、CLI や他の操作手段への切り替えは行わない。
- 必要な作成・更新・一時停止・検証・有効化ツールと、上記のプロバイダー別設定を扱えるか確認する。必要な設定を指定・検証できないことが分かった場合は、スケジュールを作成しない。

### 1. 対象の特定(要ユーザー確認)

- 発話から agent ID(または short ID)が取れればそれを使う。
- 取れない場合は `paseo_list_agents` → `paseo_get_agent_status` / `paseo_get_agent_activity` から「制限で停止しているエージェント」を推定する。
- スケジュール作成は外部副作用である。作成前に**対象をユーザーに確認する**。誤ったエージェントへの送信は取り返しがつかない。

### 2. 事前状態確認

送信の重複や実行中の work 破壊を防ぐため、作成前に 3 点を確認する。

- `paseo_get_agent_status`: status が running、または `requiresAttention` がある場合は作成・送信しない(実行中の turn は `send_agent_prompt` で置き換えられてしまう)。
- `paseo_get_agent_activity`: 最新 activity の末尾に制限通知があることを確認する(停止理由の裏取り)。
- `paseo_list_pending_permissions`: 対象に承認待ちがあれば、スケジュールを作らずその旨をユーザーに報告する。

いずれかの取得に失敗した場合は、状態不明のまま作成・送信しない。承認拒否の場合は、同じ操作を再試行したり別経路で迂回したりせず、取得できなかった項目を報告して中止する。

### 3. リセット時刻と再開予定時刻の決定

- ユーザー報告のリセット時刻を採用する。例: 「23:10 にリセット」。
- タイムゾーンを確認する。報告だけでは判断できない場合はユーザーに尋ねる(既定のタイムゾーンを暗黙に決めつけない)。
- 再開予定時刻は、リセット日時に5分を加算した日時とする。例: 2026-09-23 23:10 JST にリセット → 同日 23:15 JST に再開。日付・月・年をまたぐ場合も、加算後の日時を使う。
- リセット時刻が既に過去でも、再開予定時刻が未来なら、その時刻にスケジュールを作成する。依頼を受けた時刻から5分を数え直さない。
- 再開予定時刻に到達している場合は、即時再開(`paseo_send_agent_prompt` を直接送る)が候補になる。ただし**ユーザーに確認してから**実行し、手順 2 の状態確認は必ず済ませる。

### 4. スケジュール作成

未検証の起動設定で再開 prompt が送られることを防ぐため、仮 prompt で作成し、一時停止中に設定・検証を済ませる。再開予定時刻に間に合わない場合は有効化せず、手順 3 の即時再開の確認に戻る。

1. `paseo_create_schedule` で new-agent の単発スケジュールを作成する。初期 prompt は次の仮 prompt とする。

   ```
   このスケジュールは設定検証中です。ツールを呼び出さず、エージェントへの送信、
   リポジトリの編集、権限承認も行わないでください。「設定検証中」と報告して終了してください。
   ```

2. 返された schedule ID を使い、直ちに `paseo_pause_schedule` で一時停止する。`paseo_inspect_schedule` で停止状態と未発火を確認する。仮 prompt が既に発火していた場合は中止し、同じスケジュールで再実行しない。
3. 停止中に `paseo_update_schedule` でプロバイダー別の mode を設定する。必要な権限・feature の更新が現在の MCP でサポートされる場合は、それらも設定する。最後に `prompt` を以下のヘルパー用テンプレートに置き換える。
4. 手順 5 の検証に合格した場合だけ `paseo_resume_schedule` で有効化する。更新・検証に失敗した場合は再開せず、停止した schedule ID と理由を報告する。停止操作自体に失敗した場合も、本番 prompt に置き換えず中止する。

作成時の共通設定:

- `cron`: 手順 3 の再開予定時刻から単発 cron を組む。例: リセットが 2026-09-23 23:10 JST → 再開が同日 23:15 JST → `15 23 23 9 *`。リセットが 2026-09-30 23:58 JST なら、再開は翌月 2026-10-01 00:03 JST → `3 0 1 10 *`。
- `timezone`: 手順 3 で確認したもの(例: `Asia/Tokyo`)
- `maxRuns: 1`
- `expiresIn`: 再開予定時刻まで持ち、かつ発火後 1 時間以上の余裕がある相対時間。単発cronは年 1 回発火するため、失効設定がないと無意味なスケジュールが残る。
- ヘルパー設定: provider/model は caller を継承し、保存された値を確認する。`cwd` は対象エージェントの cwd、`isolation: local`。mode・feature は上記のプロバイダー別設定に従う。
- `name`: 例 `resume-<対象のshort-id>-agent`

ヘルパーの prompt テンプレート(対象 ID・確認した制限通知・再開予定日時を埋めて使う):

```
対象エージェント (<agent-id>) を <再開予定日時・タイムゾーン> 以降に再開してください。
確認済みの制限通知: <制限通知とその時点を特定する情報>
リポジトリは編集せず、対象や他のエージェントの権限も承認しないでください。
使用するツールは Paseo MCP の次の4つだけです。ヘルパー自身の自動審査で拒否された場合や、
ツールの承認確認・取得エラー・不明な状態が生じた場合は、送信せず理由を報告して終了してください。
拒否された操作を再試行したり、CLIなど別経路で迂回したりしないでください。

1. get_agent_status で対象の状態を確認。running または requiresAttention なら
   何もせず、その理由を報告して終了。
2. get_agent_activity で最新 activity を確認。確認済みの制限通知を裏付けられない場合、
   またはその後に再開済みの形跡があれば何もせず報告して終了。
3. list_pending_permissions で対象に承認待ちがあれば送信せず報告して終了。
4. 1〜3 がすべてクリアの場合のみ、send_agent_prompt で次の 1 文を1回だけ送る:
   「レート制限がリセットされました。中断していた作業を続けてください。」
5. 送信結果が不明でも再送しない。送信したか/しないか/結果不明とその理由を1段落で報告して終了。
```

ヘルパーに編集・対象の権限承認を禁止するのは、対象の dirty worktree(作業中の未コミット変更)を保護するためである。prompt による禁止と実行権限の制約を区別し、編集不能な環境だとは断定しない。OpenCode では実行権限の制約がなく、prompt による禁止だけが安全策になる。

### 5. 作成後の検証

有効化前に `paseo_inspect_schedule` で以下を確認する。返された new-agent 起動設定を読む。更新要求が成功したという応答だけで、設定が反映されたと判断しない。

- cron と timezone が意図どおり
- `maxRuns=1`、失効日時に発火後1時間以上の余裕がある
- 停止中かつ未発火で、prompt が本番テンプレートになっている
- provider/model/cwd とプロバイダー別の mode が意図どおり
- 該当 provider 節の検証項目を、継承設定・既定値も含めて確認できる

確認できない項目があれば停止したまま中止する。停止中は `nextRunAt` が空になる場合があるため、空であることを日時不一致と決めつけない。cron/timezone から意図した次回発火日時を確認し、有効化直前にも再開予定時刻が未来であることを確認する。

有効化後に再度 `paseo_inspect_schedule` で状態を確認する。未発火なら、`nextRunAt` が再開予定時刻（リセット時刻の5分後）と一致することを確認する（UTC 表記に注意。2026-09-23 23:15 JST = 14:15Z）。不一致なら一時停止し、schedule ID と理由を報告する。既に発火した場合はその事実を報告し、再送しない。

ユーザーには schedule ID、対象 ID、再開予定日時、ヘルパーの provider/model/mode、検証結果を報告する。OpenCode の場合は、実行時の制約がなく prompt による禁止のみであることも報告する。これは起動設定の検証であり、発火後の実効権限や再開成功の確認ではない。自動審査が拒否する可能性もあるため、「必ず再開する」「再開済み」と断定しない。

発火後の再開確認はこの手順の範囲外とする。ユーザーが明示的に頼んだときのみ、対象の status/activity を確認して成否を報告する。

## 禁止事項

- 対象が実行中・要対応・承認待ちのときに prompt を送らない。
- 実行を検証する前に「再開済み」と断定しない。
- ヘルパーによる対象 worktree の変更・権限承認を許さない。
- ヘルパーの自動審査の拒否や対象の承認待ちを、再試行・CLIなど別経路・承認の迂回で解消しない。
- 設定未検証のスケジュールを有効化しない。対象エージェントや caller の権限を変更して補わない。
