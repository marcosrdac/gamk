---
work: 20261103_0041_analyses-before-decisions
branch: main
worktree: .
origin: user conversation
commit: 0d2fe8c
---

# Integrate analyses before decisions

The shared memory order now presents `analyses/` before `decisions/` after
`wiki/`. The canonical project template, generated root `AGENTS.md`, README
diagram and lists, and install-test assertions are aligned with that order.

The feature worktree was integrated into `main` with a fast-forward after the
generator check and 42 install tests passed.
