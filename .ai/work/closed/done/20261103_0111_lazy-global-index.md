---
status: done
branch: fix/lazy-global-index
worktree: .git-worktrees/lazy-global-index
origin: user conversation
---

# Make global context discovery lazy

## Objective

Keep `.ai/global/INDEX.md` as the authoritative lightweight catalog while avoiding an exploratory scan of global context during startup.

## Plan

- Update the shared consumer instructions to attempt `.ai/global/INDEX.md` directly and tolerate a missing or unreadable file.
- Document category occupancy in `global/INDEX.md` and keep the catalog maintained by GAMK.
- Add regression coverage for the instruction and index contract, regenerate the mother `AGENTS.md`, and run the relevant checks.

## Progress

- Created isolated branch and worktree.
- Inspected current instructions, global index, maintenance rules, and test layout.
- Updated the consumer template and generated mother `AGENTS.md` to attempt a direct index read without a pre-check or global scan.
- Added explicit category occupancy to `global/INDEX.md` and documented the behavior in README/wiki.
- Added regression assertions for direct loading and truthful empty-category status.
- Verified installer, worktree, PowerShell/NixOS, generator, syntax, and diff checks.

## Next action

Integrate the branch into `main`.

## Completion criteria

- Startup guidance attempts the direct index read without a preliminary existence test or global directory scan.
- Missing/unreadable global index remains non-fatal.
- The global index reports the current state of each category.
- Generator, regression tests, and diff checks pass.
- Task is closed with a log and the worktree remains ready for integration.
