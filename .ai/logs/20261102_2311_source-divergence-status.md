---
work: 20261102_2005_source-divergence-status
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Implement read-only source-divergence status

The user selected `.ai/global-manifest.json` as the consumer provenance filename. The installer now exposes an explicit `status` command through Python, Bash, and PowerShell. It compares the recorded schema, source commit/ancestry, and source URL with the source manifest and checkout reachable through `.ai/global`.

The command is intentionally read-only. It reports `current`, `not installed`, or `attention required`; it records whether the installation is `full` or intentional `local` mode, does not inspect consumer content, repair links, rewrite manifests, or perform upgrades. The structural-upgrade skill remains responsible for user-approved migration decisions.

Regression coverage now includes current, local mode, not-installed, advanced-source, schema-mismatch, missing-link, disconnected-source, Bash wrapper, and PowerShell wrapper cases. The unit suite passes 41 tests, and the NixOS PowerShell probe passes all scenarios. Next, close the task artifacts and integrate the completed branch directly into `main`.
