---
status: done
branch: feat/flatten-analysis-status
worktree: .git-worktrees/flatten-analysis-status
---

# Flatten analysis status directories

## Objective

Change the GAMK analysis area from `analyses/doing` plus `analyses/closed/{done,wontdo}` to the flat state directories `analyses/doing`, `analyses/done`, and `analyses/wontdo`, keeping the shared instructions, installers, schema, tests, and source tree consistent.

## Plan

1. Audit all structural references and classify source-only history versus live installed paths.
2. Update the canonical template, Python/Bash/PowerShell installers, schema manifest, README/wiki, and regression tests.
3. Move the existing GAMK analyses from old states to their matching flat state directories and preserve their content.
4. Regenerate root `AGENTS.md`, run the complete validation suite, and record migration guidance for existing consumers.
5. Close, integrate, push, and clean the feature worktree safely.

## Progress

- User explicitly approved the flat analysis states: `doing/`, `done/`, and `wontdo/`.
- Updated the shared template and generated root instructions to show flat analysis states.
- Updated Python, Bash, and PowerShell installers to create the new paths.
- Incremented the structural schema from 2 to 3 and updated source manifest, README, wiki, and migration guidance.
- Moved the existing completed analyses from `analyses/closed/done/` and the incorrectly placed done analysis from `analyses/doing/` into `analyses/done/`.
- Corrected relative links from moved analyses and associated decisions/tasks.
- Added regression coverage for the flat contract and absence of the old installer paths.

## Relevant history and decisions

- `.ai/decisions/20261103_1246_flatten-analysis-status.md` records the approved flat lifecycle.
- `.ai/skills/20261102_2005_structural-upgrade.md` requires source diffs to be treated as evidence and existing consumer state to be preserved; the new schema advertises the change without rewriting consumers.
- `.ai/templates/project/AGENTS.md` is canonical shared content; root `AGENTS.md` was regenerated, never hand-edited.

## Verification

- `scripts/test_install.py`: 45 tests passed.
- `scripts/test_finish_worktree.py`: 4 tests passed.
- `scripts/test_powershell_wrappers.py`: all probes passed.
- Generator `--check`, Bash syntax checks, and `git diff --check`: passed.
- No stale live installer/template/schema references to `analyses/closed` remain; remaining mentions are intentional migration guidance or regression assertions.

## Completion criteria

- New installations create `analyses/doing`, `analyses/done`, and `analyses/wontdo`.
- Shared and generated `AGENTS.md` files document the flat analysis states.
- Structural schema is incremented and manifests/docs explain that existing consumers require explicit migration.
- Existing mother analysis content is preserved under `analyses/done/`.
- Tests and static checks pass, with no stale live installer/template references to `analyses/closed`.
- Task is closed and the worktree is ready for integration.

## Next action

Integrate into `main`, run the post-integration dry-run cleanup, remove this completed worktree and merged branch, then push the final `main` commit.
