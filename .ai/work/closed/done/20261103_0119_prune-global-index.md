---
status: done
branch: fix/prune-global-index
worktree: .git-worktrees/prune-global-index
origin: user conversation
---

# Prune redundant global index guidance

## Objective

Make `global/INDEX.md` efficient to read by retaining only its catalog/status and category routing content; remove instructions already supplied by the consumer `AGENTS.md`.

## Result

Reduced the index to category status, category purpose, and GAMK maintenance responsibility. Removed duplicated startup, precedence, task relevance, and loading guidance. Updated regression coverage; 42 installer tests, generator freshness, and diff checks passed.

## Completion

Integrated into `main` and pushed to `origin/main`.
