---
origin: user conversation
work: 20261103_1246_flatten-analysis-status
branch: feat/flatten-analysis-status
worktree: .git-worktrees/flatten-analysis-status
---

# Flatten analysis lifecycle states

The user clarified that analyses should have only three flat state directories: `doing/`, `done/`, and `wontdo/`. The source previously used `analyses/closed/{done,wontdo}` and also contained a completed analysis incorrectly left under `analyses/doing/`.

The canonical template, generated root instructions, Python/Bash/PowerShell installers, source manifest, README, wiki, tests, and migration guidance now use the flat layout. The structural schema was incremented from 2 to 3. Existing consumers are explicitly not rewritten automatically; their migration must preserve legacy content and update provenance only after approval.

Both existing completed analyses were moved to `.ai/analyses/done/`, and their relative links were corrected. Validation passed with 45 installer tests, 4 cleanup tests, all PowerShell/NixOS probes, generator check, Bash syntax, and `git diff --check`.
