---
work: 20261103_0024_rename-investigations-to-analyses
branch: feat/rename-investigations-analyses
worktree: .git-worktrees/rename-investigations-analyses
origin: user conversation
---

# Rename investigations to analyses

The repository's current research structure is now `.ai/analyses/`. The shared local `AGENTS.md` template, generated root instructions, README, Bash/PowerShell installers, Python installer, tests, historical path references, and project memory records use `analyses`.

The structural schema increased from 1 to 2. New installations create `.ai/analyses/`; existing consumer projects are not renamed or overwritten automatically and require an explicit migration.

The original task slug and branch/worktree names remain unchanged as stable execution identifiers. Historical records preserve their original provenance while references to the moved directory resolve through `.ai/analyses/`.

Verification:

- `scripts/generate_mother_agents.py --check` passed.
- `scripts/test_install.py`: 42 tests passed.
- `scripts/test_powershell_wrappers.py`: all probes passed.
- Bash syntax and `git diff --check` passed.
