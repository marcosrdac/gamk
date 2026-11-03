---
status: done
branch: feat/shared-worktree-cleanup
worktree: .git-worktrees/shared-worktree-cleanup
---

# Shared worktree cleanup instructions

## Objective

Make the completed-worktree cleanup rule self-contained in the consumer `AGENTS.md` template. Preserve the mother repository's helper/workflow as an optional implementation aid, but do not require consumer projects to have GAMK-only files.

## Plan

1. Audit the consumer template, mother extension, installer structure, tests, and project memory for similar mother-only leakage.
2. Move the generic cleanup procedure and safety checks into `.ai/templates/project/AGENTS.md`.
3. Remove the duplicate mother-only cleanup paragraph from `.ai/templates/mother-AGENTS.extensions.md` and regenerate the root `AGENTS.md`.
4. Add regression coverage for the shared contract and absence of the mother-only workflow dependency.
5. Run generator checks, relevant tests, static checks, and record the result in the task and project log.

## Progress

- Confirmed the existing decision `.ai/decisions/20261102_2324_worktree-lifecycle.md` already requires a tool-independent shared rule.
- Found and corrected the implementation mismatch: cleanup instructions had been repeated only in the mother extension, while consumers received only the creation/lifecycle outline.
- Expanded the shared template with explicit cleanup preconditions and direct Git commands.
- Removed the mother-only workflow paragraph and regenerated root `AGENTS.md`.
- Added regression coverage preventing mother-only cleanup files and names from entering the consumer template.

## Relevant history and decisions

- User clarified on 2026-11-03 that consumer projects do not receive the mother repository's `.ai/workflows/` files; the cleanup idea must be present in `AGENTS.md` in the same way as `.git-worktrees/` creation.
- Keep consumer-shared text in `.ai/templates/project/AGENTS.md`; root `AGENTS.md` is generated and must not be edited by hand.

## Verification

- `scripts/test_install.py`: 43 tests passed.
- `scripts/test_finish_worktree.py`: 4 tests passed.
- `scripts/test_powershell_wrappers.py`: all probes passed.
- Python compilation, Bash syntax, generator `--check`, and `git diff --check`: passed.
- Audit of the consumer template found no other references to GAMK, mother-only filenames, `finish-worktree.py`, or the dated cleanup workflow.

## Completion criteria

- Consumer template explains when and how to remove a completed worktree from another checkout, including clean/merged/active-task safety conditions and non-force commands.
- Consumer template contains no GAMK-only workflow/script/path dependency.
- Mother extension contains only mother-specific instructions; generated root is current.
- Relevant tests and static checks pass.
- Task is closed and the worktree is ready for integration without leaving an active task in `.ai/work/doing/`.

## Next action

Integrate `feat/shared-worktree-cleanup` into `main`, then run the mother-only dry-run cleanup procedure from a clean `main` checkout.
