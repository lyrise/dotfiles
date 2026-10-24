---
name: memory-records
description: Use the records area of the directory pointed to by the AGENT_MEMORY_DIR environment variable as external memory, consulting point-in-time records that belong to no project (periodic reports, one-off research, decisions and their reasons, etc.) and saving them on explicit request. Research results and history from an ongoing project go in its dir under projects/, following the memory-projects skill. The user archives old records by hand.
---

# Working with Records

`AGENT_MEMORY_DIR` points to a directory inside an Obsidian vault. Read and write notes directly through file operations.

## Layout

```
$AGENT_MEMORY_DIR/records/    # Immutable. Point-in-time records that are never changed once written
├── YYYY-MM-DD-<topic>.md
└── archived/                 # Old records replaced by a newer record on the same topic
    └── YYYY/
        └── MM/
            └── YYYY-MM-DD-<topic>.md
```

- `records/` holds point-in-time facts that belong to no project: periodic reports, one-off research, decisions and their reasons, and so on. Express the kind with the frontmatter `tags`, and give each note a `date`.
- Put research results and work history from an ongoing project in its dir under `projects/`, following the `memory-projects` skill, not here.
- Put knowledge that is still valid in `$AGENT_MEMORY_DIR/knowledges/`, following the `memory-knowledges` skill.
- Do not put records specific to one repository in `records/`; put them in documents inside that repository.

## Reading

- Search `records/` only when past records related to the topic are needed, and read only the notes you need.
- Treat `records/` as the content at the time of recording. Check current facts against the original sources or the current code as needed.
- Open `records/archived/YYYY/MM/` only when history or comparison with the past is needed.

## Saving

- Write only when the user explicitly asks.
- Do not rewrite a note in `records/` after it is created. Write corrections and follow-ups as a new note with a new date.
- Before saving to `records/`, search for existing records on the same topic.
- Even when a new record replaces an old one on the same topic, such as a periodic news report, do not move, copy, or delete the old record. The user archives it by hand. After saving the new record and checking its content, include in the answer the path of the old record to archive and its destination `records/archived/YYYY/MM/`. Use the date in the old record's file name for `YYYY/MM`.

## Constraints

- When `AGENT_MEMORY_DIR` is unset, or the directory it points to does not exist, report that reading or saving could not be done and stop. Do not guess a path, do not create the directory, and do not switch to the Codex, Claude, or Serena Memory.
- Read and write only inside `$AGENT_MEMORY_DIR/records/`. Do not touch other parts of the vault, such as `.obsidian/`.
- Do not use the Obsidian MCP.
