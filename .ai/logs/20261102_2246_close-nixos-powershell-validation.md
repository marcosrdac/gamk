---
work: 20261102_2200_validate-windows-installers
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Close NixOS PowerShell pre-validation

The user accepted the NixOS `pwsh` probe as the completed scope for the current validation task. The task now records the wrapper evidence as done and explicitly avoids claiming native Windows support. A separate planned task tracks Windows-host or Windows-CI validation of NTFS links, permissions, and junction fallback.

The README now exposes the NixOS command and states its limits. The active task was completed so the feature can be integrated; the native Windows task remains in `work/next/` and is not a merge blocker for this scope.
