---
name: memory-projects
description: Use the projects area of the directory pointed to by the AGENT_MEMORY_DIR environment variable as a workspace, placing documents, scripts, and raw data in a per-project dir (YYYY-MM-DD-<slug>). Research results and history from an ongoing project also go in that dir. Move completed or suspended projects to projects/archived/YYYY/MM/. Create a dir only when the user explicitly asks.
---

# Working with Projects

`AGENT_MEMORY_DIR` points to a directory inside an Obsidian vault. Read and write notes directly through file operations.

## Layout

```
$AGENT_MEMORY_DIR/projects/
├── YYYY-MM-DD-<slug>/        # Ongoing project. The date is the creation date; the slug may be Japanese, as in records/
│   ├── YYYY-MM-DD-<slug>.md  # Index note (required). The file name matches the dir name
│   └── ...                   # Documents, scripts, raw data, etc. Arrange freely
└── archived/
    └── YYYY/                 # Completed or suspended projects. YYYY is the year of the date in the dir name
        └── MM/               # MM is the month of the date in the dir name
            └── YYYY-MM-DD-<slug>/
```

- Give the index note the same file name as the dir. `[[wikilink]]` resolves by file name, so links survive a move to archived.

## Index Note

frontmatter:

```yaml
---
title: Go independent with pxna # Required. Display name
status: active # Required. active / hold / done
created: 2026-10-13 # Required. Must match the date in the dir name
updated: 2026-10-13 # Required. Date the body was last changed
---
```

The body sections are `## Purpose` `## Current State` `## Next Step` `## Related`. Omit sections that do not apply. Put `[[wikilink]]`s to related records, knowledge notes, and todo.md under `## Related`.

When the vault's existing notes use Japanese headings, use the Japanese equivalents instead and keep the language of the existing notes:

| English | Japanese |
| --- | --- |
| `## Purpose` | `## 目的` |
| `## Current State` | `## 現状` |
| `## Next Step` | `## 次の一手` |
| `## Related` | `## 関連` |

## Reading

- Before working, read the index note of the relevant project and check its current state and next step.
- If it is unclear which project the work belongs to, ask the user.

## Creating and Updating

- Create a project dir only when the user explicitly asks. Before creating one, check `projects/` and `projects/archived/` for a dir with the same purpose.
- Put research results and work history from an ongoing project inside the project dir, not in `records/`. `records/` is only for records outside projects (the `memory-records` skill).
- Put reusable knowledge and the user's own policies in `knowledge/`, following the `memory-knowledge` skill.
- Move a completed or suspended project to `projects/archived/YYYY/MM/` only after showing the path and destination and getting the user's approval. Use the date in the dir name for `YYYY/MM`.
- Ask the user before adding raw data that would bloat the repository (audio, video, large CSVs, etc.).
- Move a script reusable across projects to `scripts/` at the vault root only after showing the path and reason and getting the user's approval.
- For a project with a code repository, the documents in that repository are primary. Use the projects dir as a hub for plans, progress notes, and links within the vault.

## Constraints

- When `AGENT_MEMORY_DIR` is unset, or the directory it points to does not exist, report that the work could not be done and stop. Do not guess a path, do not create the directory, and do not switch to the Codex, Claude, or Serena Memory.
- Read and write only inside `$AGENT_MEMORY_DIR/projects/`. Do not touch other parts of the vault, such as `.obsidian/`.
- Do not use the Obsidian MCP.
