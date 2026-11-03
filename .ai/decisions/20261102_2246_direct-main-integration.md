# Decision: integrate completed work directly into `main`

- **Status:** Confirmed by user in conversation on 2026-11-02.
- **Originating work:** `20261102_2243_rename-git-worktrees`.
- **Branch/worktree:** `feat/git-ai-global-mother` / `.git-worktrees/git-ai-global-mother`.

## Decision

Use feature branches and dedicated worktrees for safe implementation, then integrate completed work directly into `main`. Do not create or use a `dev` branch for this repository unless the user explicitly requests one.

## Procedure

Before integration, the feature task must be complete, `.ai/work/doing/` must be empty, tests must pass, and the main worktree must be clean. Commit the feature branch, then fast-forward or merge it into `main` and verify both branch state and project tests.

## Consequences

The repository keeps isolation during implementation without maintaining an intermediate integration branch. Unfinished or deferred work remains documented in `.ai/work/next/` rather than being hidden in an integration branch.
