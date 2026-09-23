---
name: paseo-resume
description: Paseo でエージェントがレート制限・使用制限(usage limit / rate limit / limit reset)で停止した際、リセット時刻に自動で再開させる手順。対象エージェントの状態と承認待ちの確認、重複送信の防止、単発スケジュールの作成と検証を扱う。「レート制限で止まった」「リセットされたら再開して」「23:10 に制限リセット」「limit reset at 23:10」「使用制限がかかったから後で続けて」など、Paseo エージェントの制限解除後の再開・遅延再開を頼まれたときに必ず使用する。
---

# Paseo エージェントのレート制限リセット後の遅延再開

Paseo のエージェントがレート制限で停止したとき、リセット時刻まで人間が再 prompt し続けるのは非生産的である。この手順では、リセット時刻に単発で発火するスケジュールを作成し、ヘルパーエージェント経由で対象の既存会話を継続させる。Paseo ツールの詳細な仕様は paseo スキルを参照すること。

## 重要な前提(なぜこの手順なのか)

- `create_heartbeat` は使えない。heartbeat は呼び出し元自身を再 prompt する仕組みで、対象エージェントを指定する引数が存在しない。agent-scoped session が前提になる。
- `create_schedule` は新しいエージェント(ヘルパー)を起動する。既存会話の継続は、ヘルパーが `paseo_send_agent_prompt` に対象の agent ID を送ることで実現する。`send_agent_prompt` は対象の既存 conversation を継続できる。
- スケジュールは作成者(caller)の session mode を継承する。plan mode の caller から作るとヘルパーも plan mode になり、prompt 送信ができない。`featureValues.plan_mode=false`(または `modeId` を build に)を必ず明示する。実際に、plan mode の caller から作成したスケジュールが再開に失敗した事例がある。

## 手順

### 1. 対象の特定(要ユーザー確認)

- 発話から agent ID(または short ID)が取れればそれを使う。
- 取れない場合は `paseo_list_agents` → `paseo_get_agent_status` / `paseo_get_agent_activity` から「制限で停止しているエージェント」を推定する。
- スケジュール作成は外部副作用である。作成前に**対象をユーザーに確認する**。誤ったエージェントへの送信は取り返しがつかない。

### 2. 事前状態確認

送信の重複や実行中の work 破壊を防ぐため、作成前に 3 点を確認する。

- `paseo_get_agent_status`: status が running の場合は送信しない(実行中の turn は `send_agent_prompt` で置き換えられてしまう)。`requiresAttention` の有無も確認する。
- `paseo_get_agent_activity`: 最新 activity の末尾に制限通知があることを確認する(停止理由の裏取り)。
- `paseo_list_pending_permissions`: 対象に承認待ちがあれば、スケジュールを作らずその旨をユーザーに報告する。

### 3. リセット時刻の決定

- ユーザー報告のリセット時刻をそのまま採用する。例: 「23:10 にリセット」。
- 報告時刻が既に過去の場合は、即時再開(`paseo_send_agent_prompt` を直接送る)が候補になる。ただし**ユーザーに確認してから**実行し、手順 2 の状態確認は必ず済ませる。
- タイムゾーンを確認する。報告だけでは判断できない場合はユーザーに尋ねる(既定のタイムゾーンを暗黙に決めつけない)。

### 4. スケジュール作成

`paseo_create_schedule` で new-agent のヘルパーを単発作成する。

- `cron`: リセット時刻から単発 cron を組む。例: 2026-09-23 23:10 JST → `10 23 23 9 *`
- `timezone`: 手順 3 で確認したもの(例: `Asia/Tokyo`)
- `maxRuns: 1`
- `expiresIn`: 発火時刻まで持ち、かつ発火後 1 時間以上の余裕がある相対時間。単発cronは年 1 回発火するため、失効設定がないと無意味なスケジュールが残る。
- ヘルパー設定: provider/model は caller を継承、`cwd` は対象エージェントの cwd、`isolation: local`、`plan_mode=false`(または `modeId` を build に)
- `name`: 例 `resume-<対象のshort-id>-agent`

ヘルパーの prompt テンプレート(対象 ID・時刻を埋めて使う):

```
対象エージェント (<agent-id>) を再開してください。リポジトリは編集せず、権限も承認しないでください。

1. paseo_get_agent_status で対象の状態を確認。running または requiresAttention なら
   何もせず、その理由を報告して終了。
2. paseo_get_agent_activity で最新 activity を確認。制限通知の後に再開済みの形跡が
   あれば何もせず報告して終了。
3. paseo_list_pending_permissions で対象に承認待ちがあれば送信せず報告して終了。
4. 1〜3 がすべてクリアの場合のみ、paseo_send_agent_prompt で次の 1 文を送る:
   「レート制限がリセットされました。中断していた作業を続けてください。」
5. 送信したか/しないかとその理由を 1 段落で報告して終了。
```

ヘルパーに編集・承認を禁止するのは、対象の dirty worktree(作業中の未コミット変更)を保護するためである。

### 5. 作成後の検証

`paseo_inspect_schedule` で以下を確認し、ユーザーに報告する。

- cron と timezone が意図どおり
- `nextRunAt` がリセット時刻と一致(UTC 表記に注意。23:10 JST = 14:10Z)
- `maxRuns=1`、plan mode が無効になっていること

発火後の再開確認はこの手順の範囲外とする。ユーザーが明示的に頼んだときのみ、対象の status/activity を確認して成否を報告する。

## 禁止事項

- 対象が実行中・要対応・承認待ちのときに prompt を送らない。
- 実行を検証する前に「再開済み」と断定しない。
- ヘルパーによる対象 worktree の変更・権限承認を許さない。
