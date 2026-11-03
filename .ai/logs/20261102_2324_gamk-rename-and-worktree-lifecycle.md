---
work: 20261102_2319_rename-project-to-gamk
branch: feat/gamk-rename
worktree: .git-worktrees/gamk-rename
origin: user conversation
---

# Rename GAMK and standardize worktree closure

The user selected **GAMK — Git Agent Memory Kit** as the public name. The implementation now writes GAMK manifest identifiers while accepting the previous `git-ai-global` identifiers for existing consumers. The README was expanded into a complete guide covering the mental model, installation modes, safe migration, status checks, provenance, testing, and Windows limits.

The user also clarified that worktree cleanup must be a basic rule for every project. The shared consumer `AGENTS.md` template now requires closing the task, integrating the branch, checking cleanliness and active work, removing the worktree from another base checkout, deleting only an already-merged branch, and pruning stale records. The mother repository adds a dry-run-first helper and workflow that never uses force cleanup.

Validation includes the existing installer suite, a new four-case cleanup-helper suite, PowerShell/NixOS probes, generator checks, and static checks. The old completed worktree passes the helper's dry run; the current dirty/active worktree is correctly refused without changes.
