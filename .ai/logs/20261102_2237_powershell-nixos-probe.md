---
work: 20261102_2200_validate-windows-installers
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# PowerShell wrapper probe on NixOS

PowerShell Core was fetched temporarily with `nixpkgs#powershell` and run together with Nix-provided Python. The new `scripts/test_powershell_wrappers.py` runner passed parsing checks and exercised both `.ps1` entrypoints using temporary targets, including paths containing spaces.

The probe passed read-only `plan`, full install, blocked full install, clean copy-only install, blocked copy-only install, and `plan-mother`. It verified no-write behavior for blocked cases and the expected Linux symlink for the full install.

The probe exposed a real exit-code issue in `copy-install.ps1`: `$ErrorActionPreference = 'Stop'` caused `Write-Error` to terminate before the explicit `exit 2`. Both refusal messages now use `-ErrorAction Continue`, preserving the documented blocked-install code while still reporting the error. The probe passes after this fix.

This validates PowerShell parsing and wrapper behavior from NixOS only. It does not validate Windows `os.name == "nt"`, `cmd.exe mklink /J`, NTFS junctions, Windows permissions, or Windows path semantics. Native Windows validation remains open in this task.
