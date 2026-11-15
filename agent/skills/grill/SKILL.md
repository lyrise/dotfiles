---
name: grill
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.

Keep asking until all material decisions are resolved; do not stop at an intermediate summary or an offer to continue. Ask only when a decision would materially change scope, safety, cost, or an external side effect. Reopen a decision only on request, contradictory evidence, or blocking ambiguity; explain why and reconsider only what is affected.

When material questions are resolved, summarize the agreed plan and request whole-plan approval before acting. Never distort candidates to force a menu.

## Question style

There are two styles. Pick one at the start and keep it unless I ask to switch.

- **picker**: With four or fewer distinct options, use the native picker (e.g. AskUserQuestion); otherwise ask in prose. Do not hand-roll a picker when none exists.
- **conversational**: Do not use the native picker. Ask in prose, one question at a time: state the question and why it matters, list candidate options as a short lettered list (A, B, C…) with a one-line trade-off each, and give your recommendation with its reason. Invite free-form replies — I may pick a letter, combine options, push back, ask you a counter-question, or propose something new. Answer my counter-questions and discuss before moving on; treat the decision as settled only once I clearly agree.

Choosing the style:
- If I say something like "対話的に", "AskUserQuestion を使わず", "conversational", or "no picker", use conversational. If I ask for the picker or choice UI, use picker.
- If I specify nothing, use picker when available; otherwise conversational.
- I may switch styles mid-session; apply the new style from the next question.
