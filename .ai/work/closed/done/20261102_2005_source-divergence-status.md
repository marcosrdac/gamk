---
status: done
origin: user conversation
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
---

# Design status warnings for source and installed structure divergence

## Objective

Determine how agents/users should be warned when `.ai/global-manifest.json`'s base commit/schema differs from the current global source available through `.ai/global`.

## Questions

- Which command or event should perform the comparison (`status`, `plan`, `install`, or an agent skill)?
- How should a missing/broken symlink, unavailable remote, shallow clone, or changed Git URL be reported?
- Can the warning be useful without prompting on every routine task?
- Should the check compare only commit/schema identity, or also actual template paths/content?
- How can the warning avoid treating intentional consumer customization as corruption?

## Current decision/context

The manifest will record source URL, full base commit, and structural schema/version without an absolute local path. A global upgrade skill will guide deliberate user-approved changes. No automatic update or rewrite is authorized.

## Associated investigation

- `.ai/investigations/closed/done/20261102_2248_source-divergence-status/README.md`
- `.ai/decisions/20261102_2311_source-status-command.md`
- `.ai/logs/20261102_2311_source-divergence-status.md`

## Next action

No implementation action remains; the completed branch is ready for direct integration into `main`.

## Completion criteria

- [x] Recommend a low-noise status/warning mechanism with explicit failure cases and actionable remediation.
- [x] Preserve agent-led, user-approved upgrade behavior; do not implement automatic structural updates.
- [x] Verify the Python, Bash, PowerShell/NixOS, generator, and static checks.

## Progress

- [x] Compare provenance filename options.
- [x] User selected `.ai/global-manifest.json`.
- [x] Define comparison states and exit behavior for a deliberate read-only `status` command.
- [x] Add regression coverage for current, not installed, stale commit, schema mismatch, missing link, disconnected source, Bash forwarding, and PowerShell forwarding.
- [x] Record `full` versus intentional `local` installation mode so status does not flag an expected missing link.
- [x] Preserve user-approved, agent-led upgrades; no automatic structural update or manifest rewrite was added.
