---
work: 20261103_0119_prune-global-index
branch: fix/prune-global-index
worktree: .git-worktrees/prune-global-index
origin: user conversation
---

# Prune redundant global index guidance

The global index was reduced to its non-duplicative role: category status, category purpose, and GAMK maintenance responsibility. Startup behavior, precedence, task relevance, and loading rules remain solely in the consumer `AGENTS.md`, where they already belong.

The regression test now ensures the index does not regain those redundant sections while preserving category status and safety checks. The 42-test installer suite, generator freshness, and diff checks passed.

Next: integrate into `main`, push `origin/main`, and clean the temporary worktree.
