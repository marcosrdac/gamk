# Maintaining GAMK

This repository is the canonical source for GAMK — Git Agent Memory Kit: the current `.ai/` structure, reusable personal context, consumer templates, and installation tools.

- Preserve this repository's existing `.ai/` structure unless the user explicitly approves a structural change.
- Keep `.ai/templates/project/AGENTS.md` as the canonical shared content in the GAMK source repository. Do not edit root `AGENTS.md` by hand; the mother-local workflow generates it with a separate mother-only extension. The consumer template must not list mother-only rule/skill filenames, since those files are not installed into consumer `.ai/`.
- The local consumer template is the canonical shared source. Generate the mother root `AGENTS.md` from it plus `.ai/templates/mother-AGENTS.extensions.md` using `scripts/generate_mother_agents.py`; follow `.ai/workflows/20261102_2200_update-agent-instructions.md`. This workflow and extension are mother-local; do not put them under `global/`. Generation is only for deliberate AGENTS updates, never routine installs.
- Keep consumer-specific facts and credentials out of `global/`.
- Run `plan` to inspect a target and produce a target-agent migration prompt. `install` must complete its full read-only preflight before any target write; any relevant instruction/context or destination-conflict signal blocks installation and directs the user to `plan`.
- The safe default command is `plan`; use explicit `install` to write. If the shell wrapper receives a target without a subcommand, it runs `plan`.
- A Python-free minimal first install is available as `scripts/copy-install.sh` and `scripts/copy-install.ps1`. It only copies the consumer AGENTS template and creates the standard directories for a genuinely new project; it does not provide full provenance, global linking, or migration-aware detection. Existing context must use `plan` instead. Until tested on Windows, PowerShell behavior is implemented but unverified.
- Existing target context, especially `AGENTS.md`, is migrated by the target project's own agent. The installer never overwrites or merges existing instructions.
- `install` runs without `-y` when preflight finds no known agent/context signals or occupied destinations. Any signal blocks all writes and points to `plan`; ordinary unrelated source files alone are not a conflict.
- Record a credential-free source URL, full commit, and structural schema/version in consumer provenance without storing machine-local absolute paths. Consumer `.ai/global` is a local absolute symlink and should not be committed; `repair-link` recreates it from the current mother checkout. The installer does not edit consumer `.gitignore`, `.git/info/exclude`, or the Git index; it warns the user to ignore the link before committing.
- Structural upgrades are agent-led and user-approved one change at a time. Diffs provide evidence, not authority to overwrite consumer state.
- Synchronize templates, scripts, tests, documentation, manifest schema, and AGENTS parity guidance whenever the installed structure changes.
- Do not modify separate host-level configuration unless explicitly authorized.
