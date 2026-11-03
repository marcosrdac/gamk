---
work: 20261103_0100_normalize-global-directories
branch: feat/normalize-global-directories
worktree: .git-worktrees/normalize-global-directories
origin: user conversation
---

# Normalize global context directories

Added versioned markers for `global/rules/`, `global/workflows/`,
`global/skills/`, and `global/hosts/`, so the source exposed through `.ai/global`
matches the categories documented in `global/INDEX.md`.

Updated the README tree and regression tests. Validation passed with 42
installer tests, Bash syntax checks, and `git diff --check`.
