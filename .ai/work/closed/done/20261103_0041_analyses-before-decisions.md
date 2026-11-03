---
status: done
origin: user conversation
branch: feat/analyses-before-decisions
worktree: .git-worktrees/analyses-before-decisions
---

# Put analyses before decisions

## Objective

Change the shared memory order so `analyses/` appears before `decisions/` in the AGENTS template, generated root instructions, README diagram, lists, and tests.

## Plan

1. Swap `analyses/` and `decisions/` in the canonical template and README.
2. Regenerate root `AGENTS.md` and update order assertions.
3. Run generator/install checks, integrate the worktree into `main`, and clean it safely.

## Progress

- [x] Update the canonical template and README order.
- [x] Regenerate and verify root `AGENTS.md`.
- [x] Run checks, close, merge, push, and clean the worktree.

## Relevant history and decisions

- The user explicitly chose `analyses/` before `decisions/`.
- The root instructions remain generated from `.ai/templates/project/AGENTS.md`.

## Completion criteria

- [x] The memory tree and numbered sections put Analyses before Decisions.
- [x] README diagrams, lists, and tests match the new order.
- [x] Generator/tests pass and the worktree lifecycle is complete.

## Next action

The Analyses-before-Decisions order is ready to integrate into `main`.
