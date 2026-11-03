---
work: 20261103_0024_rename-investigations-to-analyses
branch: main
worktree: .
origin: user conversation
commit: 35bbd3c
---

# Integrate analyses terminology migration

The dedicated `feat/rename-investigations-analyses` worktree was fast-forwarded into `main`. GAMK now uses `.ai/analyses/` and schema 2 for new installations, while existing consumer projects remain protected from automatic renames. The local GAMK template migration had already been integrated as the base for this work.

The completed worktree is ready for dry-run-first cleanup, followed by publication of `main`.
