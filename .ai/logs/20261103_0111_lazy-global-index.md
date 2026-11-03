---
work: 20261103_0111_lazy-global-index
branch: fix/lazy-global-index
worktree: .git-worktrees/lazy-global-index
origin: user conversation
---

# Make global context discovery lazy

GAMK now instructs consumer agents to attempt a direct read of `.ai/global/INDEX.md` during startup. A missing or unreadable link/index is non-fatal, and the agent must not perform a preliminary existence check or scan other global directories. The index remains the authoritative lightweight catalog and directs agents toward only relevant categories.

The global index now records `rules/`, `workflows/`, `skills/`, and `hosts/` as empty, with an explicit maintenance responsibility. Regression coverage checks both the instruction contract and that an `empty` declaration matches the actual directory contents.

All relevant verification passed: 42 installer tests, 4 worktree tests, PowerShell/NixOS wrapper probes, generator freshness, Bash syntax, and `git diff --check`.

Next: close the task and integrate the isolated branch into `main`.
