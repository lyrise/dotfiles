---
name: memory-todo
description: Update todo.md directly under the directory pointed to by the AGENT_MEMORY_DIR environment variable, using the projects' index notes and any available schedule information as input. Do not regenerate todo.md; respect its existing structure, policies, and priorities. Update only when the user explicitly asks.
---

# Updating the TODO

`AGENT_MEMORY_DIR` points to a directory inside an Obsidian vault. Read and write notes directly through file operations.

## Inputs

- `$AGENT_MEMORY_DIR/todo.md`: the file to update. Read it first and check the policies and priorities written in it.
- The index notes in `$AGENT_MEMORY_DIR/projects/`: the current state and next step of each project.
- Policy notes in `knowledge/me/`: input for judging priorities (e.g., career-strategy).
- Calendar and schedule information: read it only when a means of obtaining it is available. The means is not yet decided. If there is none, ask the user when the schedule matters, or update without it.

## Updating

- Do not regenerate todo.md. Keep the existing heading structure, policy text, and priorities, and add, complete, or reorder items.
- Delete completed items from todo.md. When the history is worth keeping, keep it in the relevant project dir.
- Take project items from the index note's next-step section (`## Next Step`, or `## 次の一手` in Japanese notes) and link them to the project dir with `[[wikilink]]`.
- Do not rewrite policy text. When the policy itself needs to change, show a proposed change and get the user's approval.
- After updating, briefly show the changes to todo.md (additions, deletions, reordering) in the answer.

## Constraints

- Update only when the user explicitly asks.
- Write only to todo.md. Only read `projects/` and `knowledge/`; do not change them.
- Do not consult `work/`.
- When `AGENT_MEMORY_DIR` is unset, or the directory it points to does not exist, report that the update could not be done and stop. Do not guess a path, do not create the directory, and do not switch to the Codex, Claude, or Serena Memory.
- Do not use the Obsidian MCP.
