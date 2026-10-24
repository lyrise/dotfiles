---
name: memory-knowledges
description: Use the knowledges area of the directory pointed to by the AGENT_MEMORY_DIR environment variable as external memory, consulting reusable knowledge, information about the user and other people, and knowledge of named things such as services and products, across both work and personal life, and saving, updating, and organizing it on explicit request. Follow knowledges/GUIDELINES.md for the folder layout and rules, and grow it with approval as needed.
---

# Working with Knowledge

`$AGENT_MEMORY_DIR/knowledges/` holds only knowledge that is still valid. `AGENT_MEMORY_DIR` points to a directory inside an Obsidian vault. Read and write notes directly through file operations. The folder layout, where each category goes, file names, frontmatter, and the rules for updating, merging, and deleting are defined in `$AGENT_MEMORY_DIR/knowledges/GUIDELINES.md`. If `GUIDELINES.md` does not exist yet, show the user a draft based on the template [examples/GUIDELINES.md](examples/GUIDELINES.md), and create it only after getting approval.

## Reading

- Before searching or reading notes in `knowledges/`, read `GUIDELINES.md` and open only the notes you need, following the category definitions.
- Consult it only when knowledge related to the topic is needed. If personal context is not needed, do not open the categories about the user or other people.
- When a note may disagree with current facts, check against the original sources or the current code as needed.

## Saving, Updating, and Organizing

- Write only when the user explicitly asks.
- Before writing, read `GUIDELINES.md` and decide the location and format by its rules.
- When the content fits no existing category, or the rules need to change, show the user a proposed change to `GUIDELINES.md`, update `GUIDELINES.md` only after getting approval, and then write the note. Never change `GUIDELINES.md` without approval.
- Put point-in-time records, such as research results and work history, in `$AGENT_MEMORY_DIR/records/`, following the `memory-records` skill.

## Constraints

- When `AGENT_MEMORY_DIR` is unset, or the directory it points to does not exist, report that reading or saving could not be done and stop. Do not guess a path, do not create the directory, and do not switch to the Codex, Claude, or Serena Memory.
- Read and write only inside `$AGENT_MEMORY_DIR/knowledges/`. Do not touch other parts of the vault, such as `.obsidian/`.
- Do not use the Obsidian MCP.
