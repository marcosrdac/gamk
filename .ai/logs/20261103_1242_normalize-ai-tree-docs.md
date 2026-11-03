---
origin: user conversation
work: 20261103_1242_normalize-ai-tree-docs
branch: feat/normalize-ai-tree-docs
worktree: .git-worktrees/normalize-ai-tree-docs
---

# Normalize the documented `.ai/` tree

The user noticed that the shared `AGENTS.md` tree placed lifecycle subdirectories under `decisions/`. The repository's actual structure and installer contract keep `decisions/` flat, while `analyses/` owns `doing/` and `closed/{done,wontdo}`.

The canonical consumer template now documents that structure correctly, and the generated mother `AGENTS.md` was regenerated. A regression test checks the tree block in both files so this inversion cannot silently return. The README, wiki, detailed AGENTS sections, installer directory contract, and actual tree were audited; no other comparable mismatch was found.

Validation passed: 44 installer tests, 4 cleanup tests, all PowerShell/NixOS probes, generator check, Bash syntax, and `git diff --check`.
