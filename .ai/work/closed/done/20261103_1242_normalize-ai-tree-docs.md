---
status: done
branch: feat/normalize-ai-tree-docs
worktree: .git-worktrees/normalize-ai-tree-docs
---

# Normalize the `.ai/` tree documentation

## Objective

Make the `.ai/` tree shown in the shared `AGENTS.md` instructions match the real installed directory structure and the installer contract. In particular, keep `decisions/` flat and show the lifecycle subdirectories under `analyses/`.

## Plan

1. Compare the shared tree diagram, detailed sections, README/wiki, installer directory contract, and actual repository tree.
2. Correct the canonical consumer template and regenerate the mother `AGENTS.md`.
3. Add regression coverage for the documented tree shape and check for other mismatches.
4. Run generator, installer, static, and diff checks; record the result in project memory.

## Progress

- Confirmed `.ai/decisions/` contains timestamped Markdown files directly; it has no `doing/` or `closed/` hierarchy.
- Confirmed `.ai/analyses/` contains `doing/` and `closed/{done,wontdo}`, matching its detailed section and installer contract.
- Corrected the top-level tree diagram so `analyses/` owns its lifecycle subdirectories and `decisions/` is flat.
- Added regression coverage for both the generated root and consumer template tree blocks.
- Regenerated root `AGENTS.md` and verified generator parity.

## Relevant history and decisions

- The user requested this correction after noticing the `decisions/` mismatch and asked for other similar issues to be fixed at the same time.
- `.ai/templates/project/AGENTS.md` is the canonical shared source; root `AGENTS.md` must be regenerated, never hand-edited.
- The installer creates `decisions/` flat and `analyses/doing`, `analyses/closed/done`, and `analyses/closed/wontdo`.

## Verification

- `scripts/test_install.py`: 44 tests passed.
- `scripts/test_finish_worktree.py`: 4 tests passed.
- `scripts/test_powershell_wrappers.py`: all probes passed.
- Generator `--check`, Bash syntax checks, and `git diff --check`: passed.
- Final audit found no other mismatch between the documented `.ai/` structure and the installer contract.

## Completion criteria

- The shared and generated `AGENTS.md` tree diagrams accurately show all lifecycle subtrees.
- `decisions/` is documented as flat; `analyses/` shows its actual lifecycle subdirectories.
- Tests prevent this specific class of tree-documentation regression.
- No other mismatch is found between the documented `.ai/` structure and installer contract.
- Task is closed and the feature worktree is ready for integration.

## Next action

Integrate `feat/normalize-ai-tree-docs` into `main`, run the post-integration dry-run cleanup, then remove this completed worktree and its merged branch.
