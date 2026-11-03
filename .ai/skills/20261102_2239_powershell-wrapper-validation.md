# PowerShell wrapper validation on NixOS

## When to use

Use this skill when changing or reviewing `scripts/install.ps1`, `scripts/copy-install.ps1`, their argument forwarding, or their documented exit behavior. It is also relevant when collecting Linux-side evidence for the separate Windows validation task.

## Procedure

1. Read `.ai/workflows/20261102_2237_test-powershell-wrappers-on-nixos.md`.
2. Run `nix shell nixpkgs#python3 --command python3 scripts/test_powershell_wrappers.py` from the repository root.
3. Confirm the runner covers parsing, paths with spaces, read-only planning and status, successful installation, blocked installation without mutation, copy-only installation, and `plan-mother`.
4. If a wrapper or exit-code behavior changes, update the runner and workflow in the same task, then rerun the complete Linux suite.
5. Record the exact result and keep native Windows validation open until it runs on Windows or a Windows CI runner.

## Evidence boundary

A passing NixOS probe demonstrates PowerShell Core parsing and wrapper behavior on a Linux filesystem. It does not demonstrate Windows `os.name == "nt"` behavior, NTFS symlinks or junctions, `cmd.exe mklink /J`, Windows permissions, or Windows path semantics. Never describe this probe alone as Windows support.

## Maintenance

Keep this skill, the runner, the workflow, and the Windows validation task synchronized when wrapper commands, exit codes, or coverage change.
