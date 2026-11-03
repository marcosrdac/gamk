---
status: done
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Reprioritize native Windows validation

## Objective

Move native Windows validation out of the immediate `next/` queue into `pool/backlog/`, while keeping the submodule study and source-divergence design as the next planned work.

## Plan

1. Move the native Windows task while preserving its timestamp and slug.
2. Update current task, decision, analysis, and documentation pointers.
3. Record the prioritization rationale in a decision and log.
4. Close this bookkeeping task and integrate the update directly into `main`.

## Completion criteria

- Native Windows validation is in `.ai/work/pool/backlog/` with status `backlog`.
- `010` and `020` remain in `.ai/work/next/`.
- Current project references point to the new backlog location.
- The prioritization and its rationale are recorded.
- `.ai/work/doing/` is empty before direct integration into `main`.

## Result

Native Windows validation now lives in `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md` with status `backlog`. The `010` submodule study and `020` source-divergence design remain in `work/next/`. Current project pointers, decision records, and logs were updated.
