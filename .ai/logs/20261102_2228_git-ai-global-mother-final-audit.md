---
work: 20261102_2005_git-ai-global-mother
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Final Linux and AGENTS audit

The reopened audit was completed in the isolated feature worktree. The current root `AGENTS.md` was compared with the initial commit, the consumer template, and the mother-only extension. The approved differences are the optional `.ai/global` discovery contract, project-local instruction discovery, the updated local rules/skills index guidance, and the generated mother-repository appendix. No unapproved `.ai/memory` path or mother-only filename leaked into the consumer template.

Two accidental duplications were corrected. One repeated `Project instructions` paragraph was removed from `global/templates/project/AGENTS.md`, and the root file was regenerated with `scripts/generate_mother_agents.py`. A duplicate `test_mother_commands_are_read_only_and_refuse_missing_link` definition was removed from the regression suite; an exact-once assertion now protects the shared instruction section.

Verification passed on Linux with Nix-provided Python: 33 regression tests, Python compilation, generator `--check`, exact generated-composition comparison, Bash syntax checks, mother relative-link validation, and `git diff --check`. The branch remains uncommitted and isolated. Windows PowerShell/symlink validation remains a separate planned task and is not claimed as complete.

The implementation task can now be closed. The next possible work is the explicitly queued Windows validation; no merge or push was requested.
