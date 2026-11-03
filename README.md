# GAMK — Git Agent Memory Kit

GAMK is a Git-aware kit for giving agents durable project context: instructions, memory, rules, skills, workflows, templates, provenance, and safe installation tools.

It is designed for people who want an agent to understand a project over time without silently overwriting the project's existing knowledge or configuration.

## What GAMK provides

GAMK has two roles in one repository:

1. It is the canonical source for reusable agent context under `global/`.
2. It is a conservative installer for adding that context to consumer projects.

The shared context covers the practical continuity an agent needs between sessions:

- `AGENTS.md` instructions;
- decisions and logs;
- investigations and asynchronous forms;
- mandatory rules and optional skills;
- repeatable workflows;
- templates for future project memory;
- a source manifest and an installed-project manifest.

GAMK does not make a consumer project dependent on this checkout for ordinary operation. The consumer keeps its own `.ai/` structure; the optional personal global context is connected through a local link.

## The mental model

The source repository looks like this:

```text
gamk/
├── global/                         # Reusable source context and consumer templates
│   ├── templates/project/          # Consumer AGENTS.md and starter files
│   ├── rules/                      # Shared rules
│   ├── skills/                     # Shared skills
│   ├── workflows/                 # Shared procedures
│   └── manifest.json               # Source identity and schema
├── scripts/                        # Bash, PowerShell, Python, and test entrypoints
├── .ai/                            # GAMK's own project memory
├── AGENTS.md                       # Generated mother-repository instructions
└── README.md
```

A full consumer installation looks like this:

```text
consumer-project/
├── AGENTS.md                       # Copied shared instructions
├── .ai/
│   ├── global -> /path/to/gamk/global  # Local, machine-specific link
│   ├── global-manifest.json         # Committed provenance, without an absolute path
│   ├── work/                        # Project tasks
│   ├── decisions/                   # Durable decisions
│   ├── logs/                        # Project journal
│   ├── rules/                       # Project-local mandatory rules
│   ├── skills/                      # Project-local skills
│   ├── workflows/                   # Project-local workflows
│   └── ...
└── project files
```

The `.ai/global` link is deliberately local and should normally be ignored by the consumer project's Git configuration. GAMK does not edit `.gitignore`, `.git/info/exclude`, or the Git index for you.

## Safety model

GAMK follows a read-first, explicit-write model:

- `plan` is read-only and produces a migration prompt;
- `status` is read-only and checks source/provenance divergence;
- `install` performs a complete preflight before writing anything;
- existing `AGENTS.md`, `.ai/`, agent configuration, and occupied generated destinations block installation;
- existing project context is migrated by the target project's responsible agent, with user approval;
- `repair-link` repairs a broken or stale symlink but refuses to replace a real file or directory;
- no command automatically upgrades consumer structure or rewrites the provenance manifest;
- `--yes` never bypasses the safety preflight.

This is intentional. A template diff is evidence for a migration, not permission to replace project-owned context.

## Quick start

The commands below assume you are running them from a GAMK checkout.

### A genuinely new project without Python

Use the copy-only installer when the target has no existing agent instructions or `.ai/` context:

```bash
scripts/copy-install.sh /path/to/new-project
```

On Windows PowerShell:

```powershell
./scripts/copy-install.ps1 'C:\path\to\new-project'
```

This minimal path copies the consumer `AGENTS.md` and creates the standard `.ai/` directories. It does not create a global link, a provenance manifest, or perform the full migration-aware checks.

### A full installation

Inspect first:

```bash
scripts/install.sh plan /path/to/project
```

If the target is genuinely new and the plan shows no relevant signals, install:

```bash
scripts/install.sh install /path/to/project
```

Then check the relationship between the installed project and this source checkout:

```bash
scripts/install.sh status /path/to/project
```

PowerShell uses the same commands:

```powershell
./scripts/install.ps1 plan 'C:\path\to\project'
./scripts/install.ps1 install 'C:\path\to\project'
./scripts/install.ps1 status 'C:\path\to\project'
```

If the project already has meaningful instructions or `.ai/` context, `install` stops without writing. Give the plan to the target project's agent, review the proposed migration with the user, preserve legacy material, and rerun `install` only after the approved migration is complete.

## Installation modes

| Mode | Creates shared project structure | Creates `.ai/global` | Creates `global-manifest.json` | Use when |
| --- | --- | --- | --- | --- |
| Copy-only | Minimal `AGENTS.md` and directories | No | No | Python-free first setup of a genuinely new project |
| `full` | Yes | Yes | Yes | The normal installation with personal global context |
| `local` | Yes | No | Yes | The project should use only its own `.ai/` context |
| `global` | No | Yes | No | Only the local link should be created or repaired |

Examples:

```bash
# Full installation; this is the default.
scripts/install.sh install /path/to/project

# Shared structure without a personal global link.
scripts/install.sh install /path/to/project --local

# Link-only installation using the exact destination.
scripts/install.sh install /path/to/project/.ai/global

# Equivalent explicit link-only mode.
scripts/install.sh install /path/to/project --mode global

# Repair a broken or stale link after moving the GAMK checkout.
scripts/install.sh repair-link /path/to/project
```

The manifest records `installation_mode`, so `status` can distinguish an intentionally link-free local installation from a full installation whose link disappeared.

## Command reference

### `plan [TARGET]`

Read-only preflight. It reports target paths, source commit/schema, detected signals, and a migration prompt. A missing Bash subcommand defaults to `plan`.

### `status [TARGET]`

Read-only provenance check. It compares `.ai/global-manifest.json` with the source manifest and the Git checkout reachable through `.ai/global`.

Normal results are:

- `Status: current` — the available source agrees with the recorded installation;
- `Status: not installed` — no consumer manifest or global link exists;
- `Status: attention required` — the manifest/link is incomplete or invalid, the schema differs, the source advanced or diverged, or source identity cannot be verified.

It exits zero for current/not-installed states and nonzero when attention is required. It does not inspect consumer file contents, repair links, or perform upgrades. Local mode without `.ai/global` is normal and skips source-checkout comparison.

### `install [TARGET]`

Writes only after the complete preflight is clear. The default is full mode. Use `--local`, `--mode local`, or `--mode global` as appropriate. `--yes` is accepted for compatibility but never overrides a block.

### `repair-link [TARGET]`

Repairs a broken or stale symlink to this checkout's `global/`. It refuses to replace a real file or directory and does not touch other project context.

### `plan-mother` and `init-mother`

Read-only checks for GAMK's own tracked relative link:

```text
.ai/global -> ../global
```

`init-mother` is retained as a legacy command name. Neither command creates or changes the source link.

### Copy-only commands

`copy-install.sh` and `copy-install.ps1` are intentionally smaller than the Python-backed installer. They are useful for a clean first bootstrap, not for migrating an existing project.

## Provenance and manifests

The source manifest at `global/manifest.json` identifies the source format and structural schema:

```json
{
  "format": "gamk-source",
  "schema_version": 1,
  "repository_name": "gamk"
}
```

A full or local consumer receives `.ai/global-manifest.json`:

```json
{
  "format": "gamk-consumer",
  "schema_version": 1,
  "source_url": null,
  "base_commit": "<full Git commit>",
  "installation_mode": "full"
}
```

The consumer manifest stores the source URL when one is configured, with embedded credentials removed, and the full source commit used for installation. It never stores the machine-specific absolute path to `global/`; that path exists only in the local symlink.

For compatibility, GAMK can still read the previous `git-ai-global-source`/`git-ai-global-consumer` manifest identifiers. New installations write GAMK identifiers. The user-facing project name and documentation are now GAMK, while the stable `.ai/` paths and script names remain unchanged.

## Existing projects and upgrades

GAMK does not merge or overwrite a project's existing `AGENTS.md`, `.ai/` tree, or agent configuration. The safe migration sequence is:

1. Run `plan` against the target.
2. Read the target's current instructions and memory.
3. Compare the existing structure with `global/templates/project/` and the source history.
4. Explain the benefits, costs, risks, and legacy reconstruction work.
5. Ask the user before each consequential change.
6. Preserve unapproved or project-specific material.
7. Rerun `install` after the approved migration is complete.
8. Run `status` to confirm the resulting provenance.

The structural-upgrade procedure is documented in [`20261102_2005_structural-upgrade.md`](.ai/skills/20261102_2005_structural-upgrade.md).

## Development workflow

Every substantive change is tracked in `.ai/work/`. This repository uses dedicated Git worktrees under `.git-worktrees/` and integrates completed work directly into `main`; there is no `dev` branch.

When changing shared instructions:

1. Edit `global/templates/project/AGENTS.md` for consumer-shared content.
2. Edit `.ai/templates/mother-AGENTS.extensions.md` only for mother-repository additions.
3. Run `python scripts/generate_mother_agents.py`.
4. Run it again with `--check`.
5. Verify that mother-only content did not leak into the consumer template.

Do not edit the generated root `AGENTS.md` by hand.

### Closing a completed worktree

A worktree is temporary execution space, not permanent project inventory. After its task is closed and its branch is integrated into `main`, clean it up from the main checkout:

```bash
# Dry run: validate safety conditions and show what would be removed.
nix shell nixpkgs#python3 --command python3 scripts/finish-worktree.py \
  .git-worktrees/<worktree-name>

# Apply: remove the clean worktree and delete its already-merged branch.
nix shell nixpkgs#python3 --command python3 scripts/finish-worktree.py \
  .git-worktrees/<worktree-name> --apply
```

The cleanup refuses to proceed if the current checkout is not `main`, the target is dirty, the target has active files in `.ai/work/doing/`, or its branch is not merged. It never uses force removal or force branch deletion. The full procedure is [`20261102_2321_finish-completed-worktree.md`](.ai/workflows/20261102_2321_finish-completed-worktree.md).

## Testing

Run the Python regression suite:

```bash
python3 scripts/test_install.py
```

If Python is not installed, use Nix:

```bash
nix shell nixpkgs#python3 --command python3 scripts/test_install.py
```

The PowerShell wrapper probe can also run reproducibly on NixOS:

```bash
nix shell nixpkgs#python3 --command python3 scripts/test_powershell_wrappers.py
```

The checks cover read-only planning/status, safe preflight blocking, installation modes, manifest compatibility, Bash forwarding, PowerShell parsing/forwarding, copy-only installation, and the tracked mother link.

## Windows and NixOS boundaries

PowerShell Core can be exercised on NixOS, and that is useful evidence for parsing and wrapper argument forwarding. It does not prove native Windows behavior.

Native Windows validation is still required for:

- NTFS symlink permissions;
- the `cmd.exe mklink /J` junction fallback;
- Windows path semantics;
- native PowerShell binding and filesystem behavior.

Until those scenarios run on a Windows host or Windows CI runner, GAMK describes Windows support as unverified rather than fully validated.

## Documentation map

- [`global/INDEX.md`](global/INDEX.md) — reusable global context and loading rules;
- [`gamk.md`](.ai/wiki/gamk.md) — architecture and operational reference;
- [`20261102_2005_agents-parity.md`](.ai/skills/20261102_2005_agents-parity.md) — shared/mother instruction parity;
- [`20261102_2239_powershell-wrapper-validation.md`](.ai/skills/20261102_2239_powershell-wrapper-validation.md) — NixOS PowerShell validation;
- [`20261102_2200_update-agent-instructions.md`](.ai/workflows/20261102_2200_update-agent-instructions.md) — generated instruction workflow.

## Project name and stable interfaces

The public name is **GAMK — Git Agent Memory Kit**. The name describes the complete kit rather than only its former global-link mechanism.

The following interfaces remain stable on purpose:

- consumer `.ai/` layout;
- `.ai/global-manifest.json`;
- `scripts/install.*` and `scripts/copy-install.*`;
- `.git-worktrees/` for auxiliary worktrees;
- the source `global/` directory.

This lets the project gain a clearer identity without making existing consumer paths or local workflows move unnecessarily.
