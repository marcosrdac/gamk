# Decision: make worktree cleanup a shared agent rule

- **Status:** Confirmed by the user in conversation on 2026-11-02.
- **Originating work:** `010_20261102_2319_rename-project-to-gamk`.
- **Branch/worktree:** `feat/gamk-rename` / `.git-worktrees/gamk-rename`.

## Decision

Every project-level `AGENTS.md` generated from GAMK must treat a feature worktree as temporary execution space. Completion requires closing the task, integrating its branch into the approved base branch, verifying a clean worktree, removing the worktree from another checkout, deleting only the merged branch with `git branch -d`, and pruning stale worktree records.

Cleanup must refuse or pause when the worktree is current, dirty, active in `.ai/work/doing/`, detached, or unmerged. Force removal and force branch deletion are prohibited as routine cleanup.

The mother repository additionally provides `scripts/finish-worktree.py` and a workflow for these checks. The shared rule remains tool-independent so consumer projects receive the behavior even when they do not have the mother repository's helper script.

## Rationale

Worktrees make isolation safe, but they become confusing and consume disk space if lifecycle closure is left to memory. A checklist plus refusal conditions prevents accidental loss of uncommitted work and keeps Git metadata understandable.

## Consequences

Agents must preserve a blocked or dirty worktree and explain the condition instead of forcing deletion. Completed worktrees can be removed predictably after integration, and the cleanup procedure is visible in both shared instructions and the repository workflow.
