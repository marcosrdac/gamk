---
work: 20261102_2200_validate-windows-installers
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Add PowerShell validation skill

The NixOS PowerShell probe now has a reusable mother-local skill and a local skills index. A skill was chosen instead of a mandatory rule because the procedure is relevant only when validating or changing the PowerShell wrappers; it should not interrupt unrelated repository work.

The skill points to the executable workflow and runner, defines the required coverage, and states the evidence boundary: passing through Linux `pwsh` does not establish native Windows NTFS, permission, symlink, junction, or `cmd.exe` behavior. The Windows validation task remains active until those cases run on Windows or a Windows CI runner.
