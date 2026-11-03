# git-ai-global

This repository is the canonical source for a reusable `.ai/` context structure, personal global context, and safe consumer-project bootstrap. The existing memory structure here is preserved. Root `global/` contains reusable personal context and templates.

## Commands

Requires Python 3.10+ and Git. Shell wrappers use Nix when Python is unavailable and Nix is installed.

### Minimal first install (no Python)

For a genuinely new project with no existing agent instructions or `.ai/` context, use the copy-only installer. It uses only Bash/core utilities on Unix-like systems or built-in PowerShell on Windows:

```sh
scripts/copy-install.sh /path/to/new-project
```

```powershell
./scripts/copy-install.ps1 'C:\path\to\new-project'
```

This intentionally copies only the consumer `AGENTS.md` and creates the standard `.ai/` directories. It refuses common existing context signals and does not overwrite. It does **not** create the personal global link or a provenance manifest. For broader detection, a tailored migration prompt, full provenance, or link repair, use the Python-backed `plan`/`install` commands below. If project context already exists, do not use the copy-only path; run `plan` and migrate with the target project's agent first.

```sh
# Read-only plan, prints a contextual migration prompt and source commit. No command defaults to writing.
scripts/install.sh plan /path/to/project

# Read-only provenance/source check; returns nonzero when attention is needed.
scripts/install.sh status /path/to/project

# Installs only when preflight detects no existing agent/context signals.
scripts/install.sh install /path/to/new-project

# Install shared structure without the personal link, or install only the link.
scripts/install.sh install /path/to/project/.ai/global
scripts/install.sh install /path/to/new-project --local

# Repair a broken local consumer link after moving this checkout.
scripts/install.sh repair-link /path/to/project

# Verify this repository's tracked relative `.ai/global -> ../global` link (read-only).
scripts/install.sh plan-mother
# Legacy command name; also read-only and fails if the tracked link is missing/wrong.
scripts/install.sh init-mother
```

PowerShell equivalent:

```powershell
./scripts/install.ps1 plan 'C:\path\to\project'
./scripts/install.ps1 status 'C:\path\to\project'
./scripts/install.ps1 install 'C:\path\to\new-project'
./scripts/install.ps1 repair-link 'C:\path\to\project'
```

Windows behavior is implemented as symlink creation with junction fallback, but PowerShell binding and junction behavior still require validation on a Windows host before claiming Windows support is verified.

The Linux/NixOS pre-validation can be rerun with `nix shell nixpkgs#python3 --command python3 scripts/test_powershell_wrappers.py`. It checks PowerShell parsing, wrapper argument forwarding, no-write behavior, and Linux-side installation only; it does not validate native Windows NTFS links or permissions.

`plan` never writes to the target. `install` runs full preflight before any target write; if it detects existing agent instructions/configuration, an existing `.ai/`, or occupied destinations, it exits nonzero, lists the evidence, and prints how to request planning. It does not attempt semantic migration. The target project's agent should read the existing and new instructions, prepare a migration with the user, preserve legacy context, and integrate an existing `AGENTS.md`. Rerun `install` only after that work is done; preflight always runs again. `--yes` never bypasses preflight.

`status` is read-only. It compares `.ai/global-manifest.json` with the source manifest and Git checkout reachable through `.ai/global`, checking the structural schema, recorded source commit, commit ancestry, and source URL when available. A manifest from `--mode local` records that no personal global link is expected, so status reports that normal mode and skips checkout comparison. It does not inspect or modify consumer files beyond those provenance/link checks. It returns success for a current or not-yet-installed consumer, and nonzero with an actionable finding when the link, manifest, schema, or source identity needs attention.

If no relevant signals exist, the default install creates the structure, root `AGENTS.md`, provenance manifest, and a local absolute symlink `.ai/global` to this checkout's `global/`. `--mode local`/`--local` omits that personal link; pass the exact `.ai/global` destination to install only the link. Existing `.ai/global` is never replaced by `install`; use `repair-link` after reviewing it. Repair refuses to replace a real file/directory and repairs broken or stale symlinks.

The consumer manifest `.ai/global-manifest.json` records the installation mode, source Git URL (if configured), source commit, and structure schema version. Embedded URL credentials are stripped; prefer a credential-free Git URL. The manifest contains no machine-specific absolute path. The absolute target is necessarily stored in the local symlink itself. The installer does **not** edit `.gitignore`, `.git/info/exclude`, or the Git index. Before committing consumer changes, the user must ignore `.ai/global` locally or through their own project policy.

This mother repository uses a tracked relative link: `.ai/global -> ../global`. `plan-mother` and the legacy-named `init-mother` only verify it; neither creates nor modifies the source checkout. If missing or wrong, inspect and repair it manually, then stage it as ordinary repository content. The installer performs no Git operations. Never use consumer `install` on this mother repository; the preflight blocks it.

## Existing project structure and migrations

The installer deliberately does not copy over an existing `.ai/` tree or merge an existing `AGENTS.md`. The migration prompt includes absolute paths in the target and source, detected signals, and the full source commit. Ask the agent currently responsible for the target repository to inspect its current instructions, context and legacy files, compare them with this repository's template, explain consequences and tradeoffs, and ask before each consequential structural change. Do not delete residual legacy material merely to match the template.

For deliberate upgrades, use `.ai/skills/20261102_2005_structural-upgrade.md`. The source diff is evidence for the agent; it is not authorization to overwrite. The skill requires the agent to compare the recorded base, current consumer state, and proposed structure, then seek user approval per change.

## Maintenance

- Keep the current root `.ai/` structure authoritative unless the user approves changes.
- Keep the shared operating contract in root `AGENTS.md` and `global/templates/project/AGENTS.md` aligned. Mother-only rule/skill filenames stay out of the consumer template. The shared startup instructions require reading `.ai/global/INDEX.md` when present and following its “Always Read” entries plus task-relevant available `rules/`, `skills/`, and `workflows/`, whether `.ai/global/` is a directory or symlink. Project-local indexes remain in project `.ai/`; the mother global index describes shared content. Read `.ai/skills/20261102_2005_agents-parity.md` before changing either source file.
- Generate root mother instructions from the shared template plus mother-only additions with `python scripts/generate_mother_agents.py`. For `--check`, it verifies the root file matches its sources without writing. See `.ai/workflows/20261102_2200_update-agent-instructions.md`; generation runs only for intentional AGENTS updates, not installation.
- When changing structure, synchronize `global/templates/project/`, `scripts/install.py`, tests, manifest schema, README, and skills/rules.
- Update `global/INDEX.md` when adding discoverable global context.
- Windows is a required target but is not considered validated until PowerShell binding and symlink/junction behavior are tested on an actual Windows host. The NixOS `pwsh` pre-validation is evidence for the wrappers only.

## Tests

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
# Or, if Python is not installed:
nix shell nixpkgs#python3 --command python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

## Deferred investigations

- Study Git submodule distribution as an alternative to local absolute consumer links: `.ai/work/next/010_20261102_2005_study-submodule-global-source.md`.
- Design a status/warning mechanism for source-versus-installed divergence: `.ai/work/doing/010_20261102_2005_source-divergence-status.md`.
