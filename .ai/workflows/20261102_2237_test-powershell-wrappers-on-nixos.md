# Test PowerShell wrappers on NixOS

This workflow probes the PowerShell entrypoints from the Linux/NixOS environment. It is a preflight for the Windows validation task, not proof of native Windows behavior.

## Run

From the repository root, run:

```bash
nix shell nixpkgs#python3 --command python3 scripts/test_powershell_wrappers.py
```

The test runner obtains `nixpkgs#powershell` and `nixpkgs#python3` temporarily when `pwsh` or Python are not already available. It uses temporary directories and does not modify the repository or a user project.

## Coverage

The probe checks:

- parsing both `.ps1` wrappers;
- `install.ps1 plan` with a target path containing spaces and no writes;
- full `install.ps1` argument forwarding and Linux symlink creation;
- read-only `install.ps1 status` after a successful install;
- blocked full installation with no partial writes;
- clean and blocked `copy-install.ps1` behavior;
- read-only `plan-mother` forwarding.

## Limits

PowerShell Core on Linux does not validate Windows-specific `os.name == "nt"` code, `cmd.exe mklink /J`, NTFS junctions, Windows permissions, or Windows path behavior. Keep the Windows task open until the same scenarios run on an actual Windows host or Windows CI runner.
