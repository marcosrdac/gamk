---
work: 20261103_0057_localize-global-rules
branch: feat/localize-global-maintenance
worktree: .git-worktrees/localize-global-rules
origin: user conversation
---

# Localize GAMK maintenance rules

Removed the duplicated `global/rules/context-loading.md` and the GAMK-specific
`global/rules/system-maintenance.md`. The first behavior is already defined by
the installed `AGENTS.md`; the second belongs to this repository's local
`.ai/rules/` and is now indexed there.

Updated the global index to describe optional personal context without
mandatory entries, adjusted the mother-only extension and generated root
instructions, and aligned the README, wiki, and installer regression tests.

Validation passed: generator, generator check, 42 installer tests, Bash syntax
checks, and `git diff --check`.
