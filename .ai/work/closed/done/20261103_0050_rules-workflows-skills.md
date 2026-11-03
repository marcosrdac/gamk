---
status: done
origin: user conversation
branch: feat/rules-workflows-skills
worktree: .git-worktrees/rules-workflows-skills
---

# Order rules, workflows, and skills

## Objective

Present the operational guidance in the order `rules/ → workflows/ → skills/`,
so mandatory constraints come before repeatable procedures and optional
capabilities.

## Plan

1. Update the canonical template and regenerate the root `AGENTS.md`.
2. Align README diagrams, lists, startup guidance, and test assertions.
3. Run checks, close the task, integrate into `main`, push, and clean the worktree.

## Progress

- [x] Update the canonical template and README order.
- [x] Regenerate and verify root `AGENTS.md`.
- [x] Run checks, close, merge, push, and clean.

## Completion criteria

- [x] The memory tree and numbered sections put Rules before Workflows before Skills.
- [x] README diagrams, lists, and tests match the new order.
- [x] Generator/tests pass and the worktree lifecycle is complete.

## Next action

The Rules-before-Workflows-before-Skills order is ready to integrate into `main`.
