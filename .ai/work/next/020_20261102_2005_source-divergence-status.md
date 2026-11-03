---
status: planned
origin: user conversation
---

# Design status warnings for source and installed structure divergence

## Objective

Determine how agents/users should be warned when the consumer manifest's base commit/schema differs from the current global source available through `.ai/global`.

## Questions

- Which command or event should perform the comparison (`status`, `plan`, `install`, or an agent skill)?
- How should a missing/broken symlink, unavailable remote, shallow clone, or changed Git URL be reported?
- Can the warning be useful without prompting on every routine task?
- Should the check compare only commit/schema identity, or also actual template paths/content?
- How can the warning avoid treating intentional consumer customization as corruption?

## Current decision/context

The manifest will record source URL, full base commit, and structural schema/version without an absolute local path. A global upgrade skill will guide deliberate user-approved changes. No automatic update or rewrite is authorized.

## Next action

Design this after the manifest schema and upgrade skill have been implemented and exercised.

## Completion criteria

- Recommend a low-noise status/warning mechanism with explicit failure cases and actionable remediation.
- Preserve agent-led, user-approved upgrade behavior; do not implement automatic structural updates.
