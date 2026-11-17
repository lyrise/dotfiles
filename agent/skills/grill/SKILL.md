---
name: grill
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.

Keep asking until all material decisions are resolved; do not stop at an intermediate summary or an offer to continue. Ask only when a decision would materially change scope, safety, cost, or an external side effect. Reopen a decision only on request, contradictory evidence, or blocking ambiguity; explain why and reconsider only what is affected.

When material questions are resolved, summarize the agreed plan and request whole-plan approval before acting.

## Question style

Conversational is the default. Use picker only when the user explicitly asks for it (e.g. "picker", "AskUserQuestion を使って", "選択式で") — at any point, including in the original request. Keep the chosen style for every question, including later rounds, unless the user asks to switch; a switch applies from the next question.

- **conversational**: Never use the picker. Ask in prose: state the question and why it matters, list candidates as a short lettered list (A, B, C…) with a one-line trade-off each, and give your recommendation with its reason. Invite free-form replies — a letter, a combination, pushback, a counter-question, or a new proposal. Answer counter-questions and discuss before moving on; treat the decision as settled only once the user clearly agrees.
- **picker**: When a question has four or fewer distinct options, use the toolset's picker (`AskUserQuestion` in Claude Code, `request_user_input` in Codex) so answering costs a keystroke. Otherwise ask in prose, and do not hand-roll a picker when none is available.

Never pad, merge, drop, or distort candidates to force a menu.
