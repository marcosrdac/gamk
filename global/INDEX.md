# Personal Global Context Index

This directory is the canonical source of optional, personal, reusable agent context. Consumer projects may link `.ai/global/` to this checkout locally; the consumer link is not shared through Git. This repository's own `.ai/global` is a tracked relative symlink to `../global`.

Personal global content must not contain consumer-project facts, repository-specific maintenance rules, or credentials. Consumer projects remain independently usable without a global link. The installed `AGENTS.md` already defines how to discover this optional context; this index only maps what is available.

## Load When Relevant

- `rules/` — personal defaults and scoped operating preferences, when present.
- `workflows/` — repeatable operational procedures.
- `skills/` — reusable procedures, including deliberate structural upgrades; inspect relevant skill content when the task calls for it.
- `hosts/` — machine-specific facts; never credentials.

Update this index when adding discoverable content.
