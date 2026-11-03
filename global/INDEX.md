# Personal Global Context Index

This directory is the canonical source of personal, reusable agent context for this repository. Consumer projects may link `.ai/global/` to this checkout locally; the consumer link is not shared through Git. This repository's own `.ai/global` is a tracked relative symlink to `../global`.

Personal global content must not contain consumer-project facts or credentials. Consumer projects remain independently usable without a global link.

## Always Read

- `rules/system-maintenance.md` — source/template/install maintenance and safety boundaries.
- `rules/context-loading.md` — shared project context versus optional personal context.

## Load When Relevant

- `skills/` — reusable procedures, including deliberate structural upgrades; inspect relevant skill content when the task calls for it.
- `rules/` — personal defaults and scoped operating preferences. Rules listed under “Always Read” are mandatory; read other applicable rules before acting in their domain.
- `workflows/` — repeatable operational procedures.
- `hosts/` — machine-specific facts; never credentials.

Update this index when adding discoverable content.
