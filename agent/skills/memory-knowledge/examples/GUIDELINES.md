# Knowledge Guidelines

`$AGENT_MEMORY_DIR/knowledge/` holds only knowledge that is still valid and reusable. Work and personal life are not separated.
Point-in-time research results, work history, and the reasons behind decisions go in `$AGENT_MEMORY_DIR/records/`.
Knowledge specific to one project or repository does not go in `$AGENT_MEMORY_DIR`; it goes in the documents inside that project or repository.

## Folder Layout

```
$AGENT_MEMORY_DIR/knowledge/
├── GUIDELINES.md
├── me/      # The user's own policies, preferences, and habits
├── people/  # People
├── things/  # Named things (services, products, organizations, places)
└── topics/  # Concepts, methods, procedures, and other knowledge that belongs to no named thing
```

| Category  | Put here                                                     | Do not put here                          |
| --------- | ------------------------------------------------------------ | ---------------------------------------- |
| `me/`     | Preferences, ways of working, decision criteria, daily habits | Temporary plans, momentary moods         |
| `people/` | Relationship, affiliation, expertise, preferences, interaction tendencies | Point-in-time events (→ records) |
| `things/` | Usage, procedures, settings, constraints, known pitfalls     | Troubleshooting history (→ records)      |
| `topics/` | Key points of concepts, methods, procedures, comparisons, established practices | Procedures for a specific thing (→ things) |

When in doubt, decide by "what is the subject of this knowledge". If the subject is the user, use `me/`; another person, `people/`; a named thing, `things/`; none of these, `topics/`.

## Note Granularity

- One note per subject, placed directly under its category.
- When the body exceeds roughly 300 lines, or has three or more aspects that are consulted independently, split it into a subfolder named after the subject. The parent note is `<slug>/<slug>.md` (e.g., `things/notion/notion.md`) and holds an overview and links to the child notes.

## File Names

- Use only lowercase ASCII letters, digits, and hyphens (kebab-case).
- For people, use the romanized `family-given` name (e.g., `yamada-taro.md`).
- Keep Japanese names and aliases in the frontmatter `title` and `aliases`.

## frontmatter

```yaml
---
title: Electric kettle # Required. Display name
aliases: [kettle, 電気ケトル] # Optional. Aliases, abbreviations, Japanese notation. Used for search and link completion
tags: [thing, kitchen] # Required. The first is the category (me / person / thing / topic). The rest are free
created: 2026-09-29 # Required. Creation date
updated: 2026-09-29 # Required. Date the body was last changed
sources: # Optional. URLs or paths of the original sources. May be omitted in me/ and people/
  - https://example.com/manual
---
```

## Body Sections

Omit sections that have no content. Do not change the heading names or their order.

- `me/`: `## Policies and Preferences` `## Reasons` `## Scope`
- `people/`: `## Overview` (relationship, affiliation) `## Expertise and Interests` `## Notes on Interaction` `## Related`
- `things/`: `## Overview` `## Usage and Procedures` `## Cautions and Known Pitfalls` `## Related`
- `topics/`: `## Key Points` `## Details` `## Related`

## Confidence

- Do not mark content confirmed against original sources or the real thing; cite the source in `sources` or with a link at the end of the line.
- Mark content inferred from multiple pieces of information with 🔶 and state the basis alongside it.
- Mark unconfirmed content, or content on which sources contradict each other, with ❓. When sources contradict, write both without leaning toward either.

## Links

- Connect notes with `[[wikilink]]`.
- Do not create index notes. To find a note, decide the category and look at that folder's listing; if it is not there, search by `title` / `aliases` / `tags`.

## Updating, Merging, and Deleting

- The body always describes only the current state. Overwrite outdated text; do not keep strikethroughs or change history.
- When the history of a change is worth keeping, write a record in `$AGENT_MEMORY_DIR/records/` and link to it from the note's `## Related`.
- Update `updated` whenever the content changes.
- Before writing, search `title` and `aliases` for an existing note on the same subject. If one is found, append to it instead of creating a new one.
- Delete, merge, or rename a note only after showing the target path and the reason and getting the user's approval. When merging, add the old name to the merged note's `aliases`.

## Do Not Write

- Credentials (tokens, passwords, private keys, PINs)
- The full text of confidential information entrusted by others. Keep to the key points and a link to the original source
