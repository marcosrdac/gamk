---
status: active
origin: user conversation
branch: feat/rename-investigations-analyses
worktree: .git-worktrees/rename-investigations-analyses
---

# Rename `investigations` to `analyses`

## Objective

Replace the repository's public terminology `investigations` with `analyses` everywhere it describes the project-memory structure.

## Scope to inspect

- Rename the `.ai/investigations/` directory and its lifecycle subdirectories.
- Update the shared `AGENTS.md` template, generated root instructions, README, workflows, skills, rules, wiki, logs, tasks, tests, and scripts that reference the path or term.
- Update indexes, examples, tree diagrams, templates, and any generated or checked-in artifacts.
- Decide how to handle historical filenames and references so the rename does not erase project history or break provenance.
- Regenerate and verify generated instructions after the terminology change.

## Constraints

This task has been promoted to `doing/`. Preserve historical records and inspect all tracked references before moving paths.

## Progress

- [x] Promoted this task from `next/` to `doing/` in its dedicated worktree.
- [ ] Inventory and update current references.
- [ ] Rename the structure, verify generated instructions, and complete the worktree lifecycle.

## Completion criteria

- Every current user-facing and operational reference uses `analyses` consistently.
- The renamed structure and generated instructions pass the repository test suite.
- Historical provenance remains understandable and no unintended compatibility break is introduced.

## Next action

Inventory every tracked `investigations` reference and classify current paths versus historical records before editing.
