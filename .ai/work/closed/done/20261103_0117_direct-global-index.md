---
status: done
branch: fix/direct-global-index
worktree: .git-worktrees/direct-global-index
origin: user conversation
---

# Make the global index agent-directed

## Objective

Keep `global/INDEX.md` concise and operational for an agent already reading it from a linked project context. Remove distribution and repository-topology explanations that do not help task execution.

## Result

Rewrote the index as direct agent guidance with category status and relevance rules. Added regression checks preserving the empty-category catalog and rejecting distribution/linkage prose. Ran 42 installer tests, generator freshness, and diff checks successfully.

## Completion

Integrated into `main` and pushed to `origin/main`.
