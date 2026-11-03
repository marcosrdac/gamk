---
origin: user conversation
work: 20261103_0234_shared-worktree-cleanup
branch: feat/shared-worktree-cleanup
worktree: .git-worktrees/shared-worktree-cleanup
---

# Make worktree cleanup consumer-shared

The user identified that the root `AGENTS.md` extension referenced the mother-only cleanup workflow, even though consumer projects do not receive that workflow. The existing project decision already required this behavior to be tool-independent and shared.

The generic worktree lifecycle in `.ai/templates/project/AGENTS.md` now includes the cleanup preconditions, direct non-force Git commands, and refusal conditions. The duplicate workflow-dependent paragraph was removed from `.ai/templates/mother-AGENTS.extensions.md`, and the generated root instructions were regenerated.

The audit found no other mother-only references in the consumer template. Regression coverage now checks both the shared cleanup contract and the absence of GAMK/helper/workflow names. All installer, cleanup-helper, PowerShell/NixOS, generator, compilation, shell-syntax, and diff checks passed.

The branch is ready to integrate into `main`; after integration, the mother-only cleanup helper can remove this feature worktree through its normal dry-run-first procedure.
