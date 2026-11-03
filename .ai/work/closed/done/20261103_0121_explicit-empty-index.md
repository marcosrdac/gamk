---
status: done
branch: fix/explicit-empty-index
worktree: .git-worktrees/explicit-empty-index
origin: user conversation
---

# Make empty global categories explicit

## Objective

Remove the remaining repository-specific wording from `global/INDEX.md` and explicitly tell the agent not to read categories marked `empty`.

## Result

Removed GAMK-specific wording, defined `empty` as no reusable context, and explicitly prohibited reading empty categories. Updated regression coverage; 42 installer tests, generator freshness, and diff checks passed.

## Completion

Integrated into `main` and pushed to `origin/main`.
