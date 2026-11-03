# Decision: keep global context optional and GAMK maintenance local

- **Status:** Confirmed by the user in conversation on 2026-11-03.
- **Originating work:** `010_20261103_0057_localize-global-rules`.
- **Branch/worktree:** `feat/localize-global-maintenance` / `.git-worktrees/localize-global-rules`.

## Decision

The installed `AGENTS.md` is the authoritative source for the context-loading protocol. The root `global/` directory contains optional personal context and does not define mandatory entries by default.

Rules about maintaining GAMK itself—its templates, installer, provenance, generator, and source structure—belong under this repository's `.ai/rules/`, not under `global/`.

## Rationale

Consumer projects may expose this repository's `global/` through a local `.ai/global` link. GAMK-specific maintenance instructions would therefore leak into unrelated projects and create an unnecessary dependency on the mother repository. The `AGENTS.md` already explains how to discover optional global context, so a global context-loading rule duplicated that contract without adding behavior.

## Consequences

- Consumer projects remain usable without `.ai/global` and do not receive GAMK maintenance rules as personal defaults.
- GAMK agents read the local maintenance rule from `.ai/rules/`.
- Future global content should be genuinely reusable personal context, with applicability documented in `global/INDEX.md`.
