# Decision: keep declared global context categories present

- **Status:** Confirmed by the user in conversation on 2026-11-03.
- **Originating work:** `010_20261103_0100_normalize-global-directories`.
- **Branch/worktree:** `feat/normalize-global-directories` / `.git-worktrees/normalize-global-directories`.

## Decision

The global source keeps the categories declared by `global/INDEX.md` present as versioned directories: `rules/`, `workflows/`, `skills/`, and `hosts/`.

## Rationale

The `.ai/global` link should expose a coherent context tree even when a category has no content yet. Empty categories are represented by `.gitkeep` markers and remain optional in behavior: `AGENTS.md` loads only relevant content.

## Consequences

Future reusable global content has an obvious destination, and the repository tree matches its index. The markers themselves do not impose any global instructions on consumer projects.
