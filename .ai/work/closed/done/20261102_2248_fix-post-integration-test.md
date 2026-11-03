---
status: done
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: post-integration verification
---

# Fix post-integration manifest test

## Objective

Make the provenance-manifest regression test follow the source repository's current `HEAD` instead of the pre-integration baseline commit.

## Plan

1. Replace the stale hard-coded commit expectation with the current source identity.
2. Rerun the full regression suite, NixOS PowerShell probe, generator check, syntax checks, link check, and whitespace check.
3. Close this task, commit the fix on the feature branch, and fast-forward it directly into `main`.

## Completion criteria

- The full 33-test suite passes from the integrated source state.
- No stale baseline commit is hard-coded in the manifest test.
- `.ai/work/doing/` is empty before the follow-up fast-forward into `main`.

## Result

The test now compares the manifest commit with `install.source_identity(REPOSITORY)[0]`, so it follows the actual source `HEAD`. All verification passed after the fix, and the task is ready for direct integration into `main`.
