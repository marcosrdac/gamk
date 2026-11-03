# Personal Global Context Index

This directory is the canonical source of optional, personal, reusable agent context. Consumer projects may link `.ai/global/` to this checkout locally; the consumer link is not shared through Git. This repository's own `.ai/global` is a tracked relative symlink to `../global`.

Personal global content must not contain consumer-project facts, repository-specific maintenance rules, or credentials. Consumer projects remain independently usable without a global link. The installed `AGENTS.md` already defines how to discover this optional context; this index only maps what is available.

## Category status

GAMK maintains this catalog. `empty` means the category currently contains no reusable context beyond its directory placeholder.

| Category | Status | Use when relevant |
| --- | --- | --- |
| `rules/` | `empty` | Personal defaults or scoped operating preferences |
| `workflows/` | `empty` | Repeatable operational procedures |
| `skills/` | `empty` | Reusable specialized procedures |
| `hosts/` | `empty` | Machine-specific facts; never credentials |

## Load When Relevant

- `rules/` — personal defaults and scoped operating preferences, when present.
- `workflows/` — repeatable operational procedures.
- `skills/` — reusable procedures, including deliberate structural upgrades; inspect relevant skill content when the task calls for it.
- `hosts/` — machine-specific facts; never credentials.

Update the category status and this index's loading map whenever adding, removing, or renaming discoverable content.
