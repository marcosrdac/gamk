---
work: 20261102_2248_fix-post-integration-test
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: post-integration verification
---

# Fix manifest test after direct main integration

The first verification from `main` exposed a stale test expectation: the provenance test still expected the repository's pre-integration baseline commit. The installer correctly recorded the current `HEAD`, so the test was changed to compare against `install.source_identity(REPOSITORY)[0]`.

After the fix, the generator check, all 33 regression tests, the NixOS PowerShell probe, Python compilation, Bash syntax, mother-link validation, and `git diff --check` passed. The correction is ready for a direct fast-forward into `main`.
