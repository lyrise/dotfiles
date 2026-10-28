---
name: paseo-resume
description: Procedure for automatically resuming a Paseo agent five minutes after the reset time when it has stopped on a rate limit or usage limit (usage limit / rate limit / limit reset). Covers checking the target agent's state and pending approvals, preventing duplicate sends, and creating and verifying a one-shot schedule. Always use when asked to resume or defer-resume a Paseo agent after its limit is lifted, e.g., "it stopped on a rate limit", "resume it once the limit resets", "limit reset at 23:10", "the usage limit hit, continue later", 「レート制限で止まった」「リセットされたら再開して」「23:10 に制限リセット」「使用制限がかかったから後で続けて」.
---

# Deferred Resume of a Paseo Agent After a Rate Limit Reset

When a Paseo agent stops on a rate limit, having a human keep re-prompting it until the reset time is unproductive. This procedure creates a schedule that fires once, five minutes after the reset time, and has a helper agent continue the target's existing conversation. See the paseo skill for the detailed specifications of the Paseo tools.

## Key Premises (Why This Procedure)

- `create_heartbeat` cannot be used. A heartbeat re-prompts the caller itself and has no argument to specify a target agent. It assumes an agent-scoped session.
- `create_schedule` launches a new agent (the helper). Continuing the existing conversation is achieved by the helper sending to the target's agent ID with `paseo_send_agent_prompt`. `send_agent_prompt` can continue the target's existing conversation.
- Creating an agent-scoped schedule may inherit the caller's mode and provider settings and features. Check the approval mode and plan mode separately. Changing only the approval mode does not necessarily disable plan mode.
- Automatic review (blanket approval in OpenCode) applies to the helper's own MCP calls. It is distinct from approving the target agent's pending approvals, and approving the target's permissions is forbidden. Automatic review does not guarantee a successful resume; if it denies a call or asks for further approval, abort the send.

## Helper Settings by Provider

Identify the helper's provider/model, and pass that provider, the target's `cwd`, and the model to use (as `settings.model`) to `paseo_inspect_provider`. The target agent and the helper do not necessarily use the same provider. Check the returned modes/features and the current argument specification of the MCP, then follow the section for the relevant provider.

Common to all providers:

- In the schedule MCP as of this writing, `create_schedule` has no mode argument; change it with `mode` in `update_schedule`. There are no arguments to change provider options or features. Do not guess and pass unpublished arguments such as `settings`, `providerOptions`, or `featureValues`. Even if extra arguments are accepted, the update may ignore them.
- `create_schedule` has no model argument either. Set the helper's model explicitly with `model` in `update_schedule` while the schedule is paused. Without it the new agent falls back to the provider's default model, which may be unrelated to the caller (for example, a small on-device VLM such as Reka Edge for OpenCode). Do not assume the model inherits from the caller.
- Set `mode` explicitly to the value in each section. After saving, confirm that the mode ID for the schedule's new-agent launch configuration (e.g., `target.config.modeId`) was saved.
- Rely on a setting that has no update path only when you can confirm, from the inherited settings and defaults, that it meets the conditions in each section. Do not judge the inherited value from a query without a model or from an empty features list alone.
- If the required mode or feature cannot be set and verified through the MCP, or the provider is disabled, abort creation. Do not compensate by changing the CLI, the SDK, global settings, or the settings of the caller or the target agent.

### Codex (`codex`)

- mode: `auto-review`. `auto` is Default Permissions, not the automatic review mode.
- Abort condition: `auto-review` is not offered or unavailable. Do not switch to `full-access`.
- Abort condition: the `plan_mode` feature is enabled. The current MCP cannot disable it, so proceed only when you can confirm that the inherited value is disabled. If the MCP supports feature updates, set it to disabled.
- Verification: mode is `auto-review` and `plan_mode` is disabled.

### Claude Code (`claude`)

- mode: `auto`. The model's classifier automatically reviews permission requests. Change to `auto` even when `plan` is inherited. Do not reuse Codex's `auto-review` or `plan_mode` feature.
- Abort condition: `auto` is not offered or unavailable. Do not switch to `bypassPermissions`.
- Abort condition: approval prompts remain, for example because of explicit ask rules or MCP tools that require user interaction, so the four required tools cannot run unattended.
- Verification: mode is `auto`, not `plan`.

### OpenCode (`opencode`)

- mode: `build` (if it exists in the list). The mode selects which agent to use; it does not specify automatic review.
- Permissions: not restricted. OpenCode has no automatic review mechanism, so unlike Codex and Claude Code, blanket approval through `auto_accept` is allowed as an exception. To keep the helper from stopping on a pending approval, `auto_accept` is always `true`.
- Abort condition: the inherited `auto_accept` cannot be confirmed to be `true` (`false` or unknown). The current MCP cannot set it, so judge by the inherited value. If the MCP supports feature updates, set `true` explicitly.
- Verification: mode is `build`, `auto_accept` is `true`, and `target.config.model` is the explicitly set model.
- The only safeguard is the prohibition in the prompt. State explicitly in the final report that there are no runtime constraints.

Sources for these specifications: [Codex Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review), [Claude Code permission modes](https://code.claude.com/docs/en/permission-modes), [OpenCode agents](https://opencode.ai/docs/agents/), [Paseo provider options](https://github.com/getpaseo/paseo/blob/main/public-docs/sdk/provider-options.md). At run time, the tool specifications and provider information of the connected Paseo take precedence.

## Procedure

### 0. Check the Paseo MCP

- First confirm that the Paseo MCP tools are visible. If they are not, report this to the user and stop.
- If the MCP is not visible, do not switch to the CLI or any other means of operation.
- Confirm that you can use the required create, update, pause, verify, and enable tools, and handle the provider-specific settings above. If it turns out that a required setting cannot be specified or verified, do not create the schedule.

### 1. Identify the Target (Requires User Confirmation)

- If an agent ID (or short ID) can be taken from the user's message, use it.
- If not, infer the "agent stopped on a limit" from `paseo_list_agents` → `paseo_get_agent_status` / `paseo_get_agent_activity`.
- Creating a schedule is an external side effect. **Confirm the target with the user** before creating it. Sending to the wrong agent cannot be undone.

### 2. Check the State Beforehand

To prevent duplicate sends and destroying work in progress, check three things before creating.

- `paseo_get_agent_status`: if the status is running, or `requiresAttention` is set, do not create or send (a running turn would be replaced by `send_agent_prompt`).
- `paseo_get_agent_activity`: confirm that the latest activity ends with a limit notice (to corroborate the reason for stopping).
- `paseo_list_pending_permissions`: if the target has pending approvals, do not create a schedule; report this to the user.

If any of these cannot be retrieved, do not create or send while the state is unknown. If approval is denied, do not retry the same operation or work around it by another route; report the items that could not be retrieved and stop.

### 3. Decide the Reset Time and the Scheduled Resume Time

- Use the reset time reported by the user. Example: "resets at 23:10".
- Confirm the time zone. If the report alone is not enough to tell, ask the user (do not implicitly assume a default time zone).
- The scheduled resume time is the reset date and time plus five minutes. Example: reset at 2026-09-23 23:10 JST → resume at 23:15 JST the same day. When the addition crosses a day, month, or year boundary, use the resulting date and time.
- Even if the reset time is already in the past, create the schedule at the scheduled resume time as long as that is in the future. Do not restart the five-minute count from the time the request was received.
- If the scheduled resume time has already been reached, an immediate resume (sending `paseo_send_agent_prompt` directly) becomes an option. However, run it **only after confirming with the user**, and always complete the state checks in step 2.

### 4. Create the Schedule

To keep the resume prompt from being sent with an unverified launch configuration, create the schedule with a placeholder prompt, and finish configuration and verification while it is paused. If it cannot be ready by the scheduled resume time, do not enable it; go back to confirming an immediate resume in step 3.

1. Create a one-shot new-agent schedule with `paseo_create_schedule`. Use the following placeholder as the initial prompt.

   ```
   This schedule is under configuration verification. Do not call any tools, send to any agent,
   edit the repository, or approve any permissions. Report "under configuration verification" and finish.
   ```

2. Using the returned schedule ID, immediately pause it with `paseo_pause_schedule`. Confirm with `paseo_inspect_schedule` that it is paused and has not fired. If the placeholder prompt has already fired, abort and do not rerun with the same schedule.
3. While it is paused, set the helper's provider and model explicitly with `paseo_update_schedule` (`provider` and `model`), and set the provider-specific mode. If updating the required permissions or features is supported by the current MCP, set those as well. Finally, replace `prompt` with the helper template below.
4. Enable it with `paseo_resume_schedule` only if it passes the verification in step 5. If an update or verification fails, do not resume it; report the paused schedule ID and the reason. If the pause operation itself fails, do not replace the prompt with the real one; abort.

Common settings at creation:

- `cron`: build a one-shot cron from the scheduled resume time in step 3. Example: reset at 2026-09-23 23:10 JST → resume at 23:15 JST the same day → `15 23 23 9 *`. If the reset is at 2026-09-30 23:58 JST, the resume is at 2026-10-01 00:03 JST in the next month → `3 0 1 10 *`.
- `timezone`: the one confirmed in step 3 (e.g., `Asia/Tokyo`)
- `maxRuns: 1`
- `expiresIn`: a relative duration that lasts until the scheduled resume time with at least one hour of margin after firing. A one-shot cron fires once a year, so without an expiry a meaningless schedule would remain.
- Helper settings: provider and model do not reliably inherit from the caller; pass the provider at creation, then set the concrete model explicitly with `update_schedule` and confirm the saved values. `cwd` is the target agent's cwd, with `isolation: local`. Mode and features follow the provider-specific settings above.
- `name`: e.g., `resume-<target short-id>-agent`

Helper prompt template (fill in the target ID, the confirmed limit notice, and the scheduled resume date and time):

```
Resume the target agent (<agent-id>) at or after <scheduled resume date, time, and time zone>.
Confirmed limit notice: <the limit notice and information identifying when it occurred>
Do not edit the repository, and do not approve permissions for the target or any other agent.
Use only the following four Paseo MCP tools. If your own automatic review denies a call, or a tool
approval prompt, a retrieval error, or an unknown state arises, do not send; report the reason and finish.
Do not retry a denied operation or work around it by another route such as the CLI.

1. Check the target's state with get_agent_status. If it is running or requiresAttention,
   do nothing; report the reason and finish.
2. Check the latest activity with get_agent_activity. If the confirmed limit notice cannot be
   corroborated, or there are signs it has already been resumed since, do nothing; report and finish.
3. If list_pending_permissions shows pending approvals for the target, do not send; report and finish.
4. Only if 1–3 all pass, send the following sentence exactly once with send_agent_prompt:
   "The rate limit has been reset. Please continue the work that was interrupted."
5. Do not resend even if the send result is unknown. Report in one paragraph whether you sent,
   did not send, or the result is unknown, and why, then finish.
```

The helper is forbidden to edit or to approve the target's permissions in order to protect the target's dirty worktree (uncommitted changes in progress). Distinguish the prohibition in the prompt from constraints on execution permissions, and do not assert that the environment cannot be edited. In OpenCode there are no constraints on execution permissions, and the prohibition in the prompt is the only safeguard.

### 5. Verify After Creation

Before enabling, check the following with `paseo_inspect_schedule`. Read the returned new-agent launch configuration. Do not conclude that a setting took effect only because the update request returned success.

- cron and timezone are as intended
- `maxRuns=1`, and the expiry leaves at least one hour of margin after firing
- It is paused and has not fired, and the prompt is the real template
- provider/model/cwd and the provider-specific mode are as intended, and `target.config.model` contains the explicitly set model rather than being empty or a provider default
- The verification items in the relevant provider section can be confirmed, including inherited settings and defaults

If any item cannot be confirmed, leave it paused and abort. While paused, `nextRunAt` may be empty, so do not treat an empty value as a date mismatch. Confirm the intended next fire time from cron/timezone, and right before enabling, confirm again that the scheduled resume time is in the future.

After enabling, check the state again with `paseo_inspect_schedule`. If it has not fired, confirm that `nextRunAt` matches the scheduled resume time (five minutes after the reset time) (mind the UTC notation: 2026-09-23 23:15 JST = 14:15Z). If they do not match, pause it and report the schedule ID and the reason. If it has already fired, report that fact and do not resend.

Report to the user the schedule ID, the target ID, the scheduled resume date and time, the helper's provider/model/mode, and the verification results. For OpenCode, also report that there are no runtime constraints and only the prohibition in the prompt. This verifies the launch configuration; it does not confirm the effective permissions after firing or a successful resume. Automatic review may also deny calls, so do not assert "it will definitely resume" or "it has resumed".

Confirming the resume after firing is outside the scope of this procedure. Only when the user explicitly asks, check the target's status/activity and report whether it succeeded.

## Prohibitions

- Do not send a prompt while the target is running, requires attention, or has pending approvals.
- Do not assert "resumed" before verifying the run.
- Do not allow the helper to change the target's worktree or approve permissions.
- Do not resolve a denial by the helper's automatic review or the target's pending approvals by retrying, using another route such as the CLI, or bypassing approval.
- Do not enable a schedule whose settings are unverified. Do not compensate by changing the permissions of the target agent or the caller.
