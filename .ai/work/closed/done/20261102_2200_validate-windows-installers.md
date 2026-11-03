---
status: done
origin: user conversation
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
related_work: ../closed/done/20261102_2005_git-ai-global-mother.md
scope: NixOS PowerShell wrapper pre-validation; native Windows validation deferred
---

# Validate PowerShell wrappers through NixOS

## Objective

Validate the PowerShell entrypoints and the Python migration-aware installer's wrapper behavior through NixOS `pwsh`, without claiming native Windows support.

## Plan

1. Run the reusable NixOS workflow and runner with Nix-provided PowerShell and Python.
2. Verify PowerShell parsing and argument forwarding with paths containing spaces.
3. Verify read-only planning, successful Linux-side installation, blocked installation without mutation, copy-only behavior, and `plan-mother`.
4. Record the evidence boundary and keep native Windows cases in a separate planned task.

## Current status

The NixOS PowerShell Core probe passes through `.ai/workflows/20261102_2237_test-powershell-wrappers-on-nixos.md` and passes. It validates parsing, argument forwarding, no-write blocking, Linux-side installation, and the mother validator. It cannot validate native Windows symlink/junction behavior; that work is deferred to `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.

## Progress

- [x] Run the PowerShell wrappers through Nix-provided `pwsh` with paths containing spaces.
- [x] Verify `plan`, full `install`, blocked `install`, clean `copy-install`, blocked `copy-install`, and `plan-mother` without repository or target partial writes.
- [x] Detect and fix the PowerShell error-handling path that returned `1` instead of the documented blocked-install code `2`.
- [x] Document the repeatable NixOS probe workflow and runner.
- [x] Add an optional mother-local skill and `.ai/skills/INDEX.md` for this validation method; no mandatory rule was added because the probe is only relevant to wrapper/platform work.
- [x] Close the NixOS pre-validation scope without claiming native Windows support.

## Completion criteria

- Both `scripts/install.ps1` and `scripts/copy-install.ps1` are exercised through NixOS `pwsh`.
- Argument forwarding, exit behavior, Linux-side link behavior, and no-write conflict behavior are evidenced.
- The README and platform claims explicitly distinguish this pre-validation from native Windows support.
