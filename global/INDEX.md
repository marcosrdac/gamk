# Global Context Index

Read this index first. Use it to decide whether global context is relevant to the current task. Do not scan categories marked `empty`; when a category is available, read only the files relevant to the task.

Project-local instructions take precedence. Do not use global context to override explicit task or user instructions. Keep project-specific facts, repository maintenance rules, and credentials out of global context.

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
- Follow any `Always Read` entries when present.

Maintenance: GAMK must update the category status and this loading map whenever adding, removing, or renaming discoverable content.
