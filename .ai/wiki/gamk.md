# GAMK architecture and operations

## Purpose and source layout

This repository is GAMK — Git Agent Memory Kit. It preserves a reusable `.ai/` continuity structure and acts as the canonical source/installer for consumer projects. The generated consumer `AGENTS.md` template is local at `.ai/templates/project/`; reusable personal context lives under root `global/`. The source repository's `.ai/global -> ../global` is a tracked relative symlink. A consumer instead has a local absolute `.ai/global` symlink to this checkout; it is machine-specific and should not be committed.

## Consumer manifest

`.ai/global-manifest.json` records the `gamk-consumer` format, installation mode, schema version, source URL (with URL credentials stripped), and full source base commit. It must not contain machine-specific absolute paths. A missing source origin is represented as `null`. Local mode intentionally has no personal `.ai/global` link. The installer still reads the legacy `git-ai-global-consumer` identifier for compatibility.

## Commands and safety

- `.ai/templates/project/AGENTS.md` is canonical shared content. `scripts/generate_mother_agents.py` generates root `AGENTS.md` by appending `.ai/templates/mother-AGENTS.extensions.md`; shared text is not duplicated. Mother-only content, including the extension, maintenance rule, and workflow, stays under `.ai/` and never under `global/`. The extension tells mother agents to read applicable local `.ai/rules/` and consult local skills/workflows. The mother-only workflow `.ai/workflows/20261102_2200_update-agent-instructions.md` governs deliberate instruction updates, not routine installs. Shared startup attempts to read `.ai/global/INDEX.md` directly, tolerates a missing or unreadable link/file, and consults only relevant categories named by the index. Global context has no mandatory entries by default.
- `scripts/copy-install.sh TARGET` (Bash) and `scripts/copy-install.ps1 TARGET` (PowerShell) provide a Python-free minimal first install for new projects. They copy consumer `AGENTS.md` and create standard directories only; they do not create provenance/global links or perform full migration detection. They refuse common pre-existing context signals.
- `plan [TARGET]` is read-only and prints target paths, source commit/schema, findings, and migration instructions. A missing subcommand in the Bash wrapper defaults to `plan`.
- `status [TARGET]` is read-only and compares `.ai/global-manifest.json` with the source manifest and Git checkout reachable through `.ai/global`. It reports `current`, `not installed`, or `attention required`; the latter covers missing/broken links, invalid provenance, schema differences, and source commit/URL divergence. A manifest recorded as local mode normally has no link and skips checkout comparison. Status exits nonzero only for attention-required cases and never modifies consumer files.
- `install [TARGET]` defaults to full installation; `--mode local` installs shared project context without the global link; `--mode global` or an exact `.ai/global` destination installs only that link. `--yes` never bypasses preflight.
- Full installation detects known root/nested agent instructions/configuration, an existing `.ai/`, and occupied generated destinations. Any signal blocks the operation before writes and points to `plan`. Ordinary project files alone are not interpreted as conflicts.
- Link-only operations inspect only the link destination. Repair replaces broken/stale symlinks but refuses to replace a real file or directory.
- The installer never modifies `.gitignore`, `.git/info/exclude`, or the Git index. It tells the user to ignore the local link before committing.
- The installer refuses to run consumer installation against the mother repository; `plan-mother`/`init-mother` maintain its relative link.

## Worktree lifecycle

Worktrees are temporary execution spaces. Every project using GAMK receives the same basic closure rule through the shared `AGENTS.md` template: close the task, integrate the branch, verify that the worktree is clean and has no active `work/doing/` task, remove it from another base checkout, delete only the merged branch with `git branch -d`, and run `git worktree prune`. Dirty, active, detached, current, or unmerged worktrees are preserved rather than force-removed.

The mother repository provides `.ai/workflows/20261102_2321_finish-completed-worktree.md` and `scripts/finish-worktree.py` for a dry-run-first implementation of those checks.

## Migration and upgrades

Existing project instructions and `.ai/` trees are never overwritten. `plan` provides a prompt for the target repository's own agent to inspect local context, explain changes and tradeoffs, preserve legacy content, and integrate an existing `AGENTS.md` responsibly. After the user approves and migration work completes, rerun install and pass preflight again.

For future schema upgrades, `.ai/skills/20261102_2005_structural-upgrade.md` requires comparing source diffs, recorded provenance, and actual target state, then asking approval for every structural change. No automatic upgrade is allowed.

## Known platform status

Linux behavior is covered by `scripts/test_install.py`. Bash syntax and wrapper invocation have been tested. Windows PowerShell argument forwarding and symlink/junction fallback have not been tested on a Windows host; Windows support remains unverified.

PowerShell Core can be probed reproducibly on NixOS with `scripts/test_powershell_wrappers.py` and the workflow `.ai/workflows/20261102_2237_test-powershell-wrappers-on-nixos.md`. That probe covers parsing, argument forwarding, no-write blocking, and Linux-side wrapper behavior, but it does not replace native Windows validation of NTFS links, permissions, or `cmd.exe` junction fallback.

## Deferred

- Native Windows installer validation: `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.
- Git submodule distribution alternative: `.ai/work/next/010_20261102_2005_study-submodule-global-source.md`.
