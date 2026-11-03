# Decision: flatten analysis lifecycle states

- **Status:** Confirmed by the user in conversation on 2026-11-03.
- **Originating work:** `005_20261103_1246_flatten-analysis-status`.
- **Branch/worktree:** `feat/flatten-analysis-status` / `.git-worktrees/flatten-analysis-status`.

## Decision

Use three flat state directories for project analyses:

- `.ai/analyses/doing/` for active or paused analyses;
- `.ai/analyses/done/` for completed analyses; and
- `.ai/analyses/wontdo/` for abandoned analyses.

Do not add a `closed/` intermediary under `analyses/`.

## Rationale

The analysis lifecycle has the same simple state model as the user's mental map: active work, completed work, or intentionally abandoned work. A flat layout reduces path depth and avoids implying that `closed/` is a separate lifecycle object.

## Consequences

The installed structure schema increments from 2 to 3. New installations create the flat directories. Existing consumers are not rewritten automatically; agents must perform an explicit, user-approved migration while preserving any existing `analyses/closed/` content and updating provenance only after migration is complete.
