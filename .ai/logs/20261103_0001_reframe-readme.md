---
work: 20261103_0001_reframe-readme
branch: feat/readme-reframe
worktree: .git-worktrees/readme-reframe
origin: user conversation
---

# Reframe README around adoption and operation

The README was reorganized to lead with the value of durable agent memory, show the GAMK-to-consumer installation flow, teach practical commands and daily agent use, and finish with repository structure and maintenance. A Mermaid flow now explains the source → plan/review/install → consumer relationship; file trees remain text for precise hierarchy.

The documentation was checked against the current installer and safety behavior. Validation passed: 42 installer tests, 4 worktree-cleanup tests, PowerShell/NixOS probes, generator `--check`, Bash syntax checks, and `git diff --check`.
