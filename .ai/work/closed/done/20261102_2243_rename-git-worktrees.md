---
status: done
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
related_work: 010_20261102_2200_validate-windows-installers
---

# Rename the repository worktree convention

## Objective

Rename the project convention and physical auxiliary worktree directory to `.git-worktrees` without losing the uncommitted feature work or stale path references.

## Plan

1. Inventory all project references and current Git worktree state.
2. Pause the active Windows validation task and checkpoint its resume path.
3. Move the linked feature worktree using Git's worktree metadata, preserving its branch and uncommitted files.
4. Update the shared consumer template, regenerate the mother `AGENTS.md`, and update repository memory, tests, and documentation references.
5. Add the new local worktree path to the main repository's local Git exclude so auxiliary files do not appear as project content.
6. Verify Git worktree registration, branch/status continuity, absence of stale previous-directory references, generator parity, and all tests.

## Progress

- [x] Inventoried all project references and Git worktree state.
- [x] Paused the Windows validation task and preserved its resume context.
- [x] Moved the linked worktree to `.git-worktrees/git-ai-global-mother` without losing uncommitted files.
- [x] Updated the shared template, regenerated `AGENTS.md`, and changed tests, decisions, logs, and task records.
- [x] Added `.git-worktrees/` to the main repository's local Git exclude.
- [x] Verified no stale previous-directory references remain in the feature worktree.
- [x] Passed generator check, 33 tests, NixOS PowerShell probe, Python/Bash checks, link validation, and whitespace checks.

## Completion criteria

- The feature worktree is registered at `.git-worktrees/git-ai-global-mother` on `feat/git-ai-global-mother`.
- Shared instructions and all live project references use `.git-worktrees`.
- Historical records are either updated consistently or explicitly explain any retained historical path.
- The main worktree remains on `main`; the feature's uncommitted implementation is preserved.
- Generator checks, the 33-test suite, the NixOS PowerShell probe, Python/Bash checks, and whitespace validation pass.
- The Windows validation task is paused and resumable after this task completes.
