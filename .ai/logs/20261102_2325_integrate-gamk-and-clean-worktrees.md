---
work: 20261102_2319_rename-project-to-gamk
branch: main
worktree: .
origin: user conversation
---

# Integrate GAMK and clean completed worktrees

The completed `feat/gamk-rename` branch was fast-forwarded directly into `main` at commit `4573001`. The shared `AGENTS.md` template now contains the generic worktree lifecycle rule, and the mother repository includes a dry-run-first cleanup helper and workflow.

From the clean main checkout, the helper validated and removed both completed worktrees: `.git-worktrees/git-ai-global-mother` and `.git-worktrees/gamk-rename`. Their already-merged branches were deleted with `git branch -d`; no force removal or force branch deletion was used. The repository now keeps only the main worktree, with the next submodule study still in `work/next/`.
