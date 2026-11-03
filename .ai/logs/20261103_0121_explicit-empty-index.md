---
work: 20261103_0121_explicit-empty-index
branch: fix/explicit-empty-index
worktree: .git-worktrees/explicit-empty-index
origin: user conversation
---

# Make empty global categories explicit

Removed the remaining GAMK-specific wording from `global/INDEX.md`. The index now states that `empty` means no reusable context exists and explicitly instructs the agent not to read categories marked `empty`. Catalog maintenance is expressed neutrally as keeping the index current when contents or usage change.

Regression coverage was updated, and the 42-test installer suite, generator freshness, and diff checks passed.

Next: integrate into `main`, push `origin/main`, and clean the temporary worktree.
