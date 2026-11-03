# git-ai-global architecture and operations

## Purpose and source layout

This repository preserves the project's `.ai/` continuity structure and acts as the canonical source/installer for consumers. Reusable personal context and consumer templates live under root `global/`. The mother repository's `.ai/global -> ../global` is a tracked relative symlink. A consumer instead has a local absolute `.ai/global` symlink to this checkout; it is machine-specific and should not be committed.

## Consumer manifest

`.ai/git-ai-global.json` records format, schema version, source URL (with URL credentials stripped), and full source base commit. It must not contain machine-specific absolute paths. A missing source origin is represented as `null`.

## Commands and safety

- `global/templates/project/AGENTS.md` is canonical shared content. `scripts/generate_mother_agents.py` generates root `AGENTS.md` by appending `.ai/templates/mother-AGENTS.extensions.md`; shared text is not duplicated. Mother-only content, including the extension and workflow, stays under `.ai/` and never under `global/`. The extension tells mother agents to read applicable local `.ai/rules/` and consult local skills/workflows. The mother-only workflow `.ai/workflows/20261102_2200_update-agent-instructions.md` governs deliberate instruction updates, not routine installs. Shared startup treats `.ai/global/` as optional whether it is a directory or symlink: read `INDEX.md`, follow “Always Read” entries (including mandatory rules), and consume relevant available categories, with task/project instructions taking precedence.
- `scripts/copy-install.sh TARGET` (Bash) and `scripts/copy-install.ps1 TARGET` (PowerShell) provide a Python-free minimal first install for new projects. They copy consumer `AGENTS.md` and create standard directories only; they do not create provenance/global links or perform full migration detection. They refuse common pre-existing context signals.
- `plan [TARGET]` is read-only and prints target paths, source commit/schema, findings, and migration instructions. A missing subcommand in the Bash wrapper defaults to `plan`.
- `install [TARGET]` defaults to full installation; `--mode local` installs shared project context without the global link; `--mode global` or an exact `.ai/global` destination installs only that link. `--yes` never bypasses preflight.
- Full installation detects known root/nested agent instructions/configuration, an existing `.ai/`, and occupied generated destinations. Any signal blocks the operation before writes and points to `plan`. Ordinary project files alone are not interpreted as conflicts.
- Link-only operations inspect only the link destination. Repair replaces broken/stale symlinks but refuses to replace a real file or directory.
- The installer never modifies `.gitignore`, `.git/info/exclude`, or the Git index. It tells the user to ignore the local link before committing.
- The installer refuses to run consumer installation against the mother repository; `plan-mother`/`init-mother` maintain its relative link.

## Migration and upgrades

Existing project instructions and `.ai/` trees are never overwritten. `plan` provides a prompt for the target repository's own agent to inspect local context, explain changes and tradeoffs, preserve legacy content, and integrate an existing `AGENTS.md` responsibly. After the user approves and migration work completes, rerun install and pass preflight again.

For future schema upgrades, `.ai/skills/20261102_2005_structural-upgrade.md` requires comparing source diffs, recorded provenance, and actual target state, then asking approval for every structural change. No automatic upgrade is allowed.

## Known platform status

Linux behavior is covered by `scripts/test_install.py`. Bash syntax and wrapper invocation have been tested. Windows PowerShell argument forwarding and symlink/junction fallback have not been tested on a Windows host; Windows support remains unverified.

PowerShell Core can be probed reproducibly on NixOS with `scripts/test_powershell_wrappers.py` and the workflow `.ai/workflows/20261102_2237_test-powershell-wrappers-on-nixos.md`. That probe covers parsing, argument forwarding, no-write blocking, and Linux-side wrapper behavior, but it does not replace native Windows validation of NTFS links, permissions, or `cmd.exe` junction fallback.

## Deferred

- Native Windows installer validation: `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.
- Git submodule distribution alternative: `.ai/work/next/010_20261102_2005_study-submodule-global-source.md`.
- Source/manifest divergence warnings: `.ai/work/next/020_20261102_2005_source-divergence-status.md`.
