---
work: 20261103_0034_localize-agents-template
branch: feat/local-agents-template
worktree: .git-worktrees/local-agents-template
origin: user conversation
---

# Localize the GAMK AGENTS template

The canonical consumer `AGENTS.md` template moved from `global/templates/project/AGENTS.md` to `.ai/templates/project/AGENTS.md`. The generator, installers, tests, parity guidance, workflows, wiki, global index, and README now use the local source path. `global/` no longer carries the template, and a consumer install receives only the generated `AGENTS.md`; a regression assertion confirms the source template is not copied into `.ai/templates/project/`.

Verification:

- `scripts/generate_mother_agents.py --check` passed.
- `scripts/test_install.py`: 42 tests passed.
- `scripts/test_powershell_wrappers.py`: all probes passed.
- Bash syntax and `git diff --check` passed.
