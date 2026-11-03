# Decision: use `.git-worktrees` for auxiliary worktrees

- **Status:** Confirmed by user in conversation on 2026-11-02.
- **Originating work:** `005_20261102_2243_rename-git-worktrees`.
- **Branch/worktree:** `feat/git-ai-global-mother` / `.git-worktrees/git-ai-global-mother`.

## Decision

Use `.git-worktrees/` as the repository convention and physical parent directory for Git-linked auxiliary worktrees. Each child directory is named for its branch or task, such as `.git-worktrees/git-ai-global-mother/`.

Update shared agent instructions, generated mother instructions, tests, live documentation, and repository memory to use this convention. Keep `.git-worktrees/` in the main repository's local `.git/info/exclude`; do not add the machine-local worktree directory to versioned project content.

## Rationale

The name makes the Git relationship explicit while remaining hidden from ordinary project listings. Moving the registered worktree with `git worktree move` preserves branch identity and uncommitted files.

## Consequences

The main worktree is clean of the auxiliary directory because the local Git exclude hides it. Consumers and future agents should create new linked worktrees below `.git-worktrees/`. Native Git metadata under `.git/` remains managed by Git and is not part of this naming convention.
