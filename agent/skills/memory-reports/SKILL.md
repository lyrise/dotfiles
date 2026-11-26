---
name: memory-reports
description: Use the reports area of the directory pointed to by the AGENT_MEMORY_DIR environment variable as external memory, consulting point-in-time reports that belong to no project (periodic reports, one-off research, decisions and their reasons, etc.) and saving them on explicit request. Research results and history from an ongoing project go in its dir under projects/, following the memory-projects skill.
---

# Working with Reports

`AGENT_MEMORY_DIR` points to a directory inside an Obsidian vault. Read and write notes directly through file operations.

## Layout

```
$AGENT_MEMORY_DIR/reports/    # Immutable. Point-in-time reports that are never changed once written
├── YYYY-MM-DD-<topic>.md
└── archived/                 # Old reports replaced by a newer report on the same topic
    └── YYYY/
        └── MM/
            └── YYYY-MM-DD-<topic>.md
```

- `reports/` holds point-in-time facts that belong to no project: periodic reports, one-off research, decisions and their reasons, and so on. Express the kind with the frontmatter `tags`, and give each note a `date`.
- Put research results and work history from an ongoing project in its dir under `projects/`, following the `memory-projects` skill, not here.
- Put knowledge that is still valid in `$AGENT_MEMORY_DIR/knowledge/`, following the `memory-knowledge` skill.
- Do not put reports specific to one repository in `reports/`; put them in documents inside that repository.

## Reading

- Search `reports/` only when past reports related to the topic are needed, and read only the notes you need.
- Treat `reports/` as the content at the time it was written. Check current facts against the original sources or the current code as needed.
- Open `reports/archived/YYYY/MM/` only when history or comparison with the past is needed.

## Saving

- Write only when the user explicitly asks.
- Do not rewrite a note in `reports/` after it is created. Write corrections and follow-ups as a new note with a new date.
- Before saving to `reports/`, search for existing reports on the same topic.

## Constraints

- When `AGENT_MEMORY_DIR` is unset, or the directory it points to does not exist, report that reading or saving could not be done and stop. Do not guess a path, do not create the directory, and do not switch to the Codex or Claude Memory.
- Read and write only inside `$AGENT_MEMORY_DIR/reports/`. Do not touch other parts of the vault, such as `.obsidian/`.
- Do not use the Obsidian MCP.
