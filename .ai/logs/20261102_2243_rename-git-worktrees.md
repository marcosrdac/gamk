---
work: 20261102_2243_rename-git-worktrees
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Rename auxiliary Git worktrees

The linked feature worktree was moved from the previous hidden directory convention to `.git-worktrees/git-ai-global-mother` with `git worktree move`. The branch, base commit, uncommitted implementation, and `.ai/` memory were preserved. The main worktree remains on `main` and its local Git exclude now hides `.git-worktrees/`.

The shared consumer template was updated and the mother `AGENTS.md` was regenerated. Tests, decisions, logs, and task metadata now point to `.git-worktrees`; no stale reference to the previous directory name remains in the feature worktree.

Verification passed: generated `AGENTS.md` is current, 33 regression tests pass, the NixOS PowerShell probe passes, Python compilation and Bash syntax checks pass, the mother relative link is correct, and `git diff --check` passes. The Windows validation task was resumed after the rename and remains open only for native Windows behavior.
