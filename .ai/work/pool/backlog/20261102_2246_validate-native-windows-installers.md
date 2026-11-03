---
status: backlog
origin: user conversation
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
related_work: ../closed/done/20261102_2200_validate-windows-installers.md
depends_on: Windows host or Windows CI runner
moved_at: 20261102_2248
previous_state: planned
backlog_reason: User decided native Windows validation is useful but not currently prioritized.
---

# Validate native Windows installers

## Objective

Validate the Windows-specific portions that cannot be proven through NixOS PowerShell Core: NTFS links, permissions, PowerShell behavior on Windows, and the junction fallback.

## Plan

1. Run `scripts/install.ps1` and `scripts/copy-install.ps1` on a Windows host or Windows CI runner with targets containing spaces.
2. Verify plan, successful install, blocked install, copy-only install, and exit-code behavior.
3. Test native symlink creation with the permitted configuration and junction fallback when symlink creation is unavailable.
4. Test repair behavior and refusal to replace a real file or directory.
5. Record Windows, PowerShell, and Python versions and update README/platform claims with evidence.

## Current status

Not run. The NixOS PowerShell workflow is complete as a wrapper pre-validation, but it does not establish native Windows support.

## Completion criteria

- Windows-specific behavior is exercised and evidenced.
- Any failures are fixed or explicitly documented.
- Documentation distinguishes tested Windows configurations from untested ones.
