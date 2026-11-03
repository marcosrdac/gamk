---
work: 20261103_0010_readme-agents-first-diagrams
branch: feat/readme-agents-first
worktree: .git-worktrees/readme-agents-first
origin: user conversation
---

# README Mermaid review gallery

## What happened

The README now presents the consumer-project model from `AGENTS.md` outward. It includes three alternative Mermaid renderings of the `.ai/` memory map, all following the order documented by the shared instructions:

1. a vertical reading path;
2. a horizontal ordered rail;
3. a responsibility map centered on `.ai/`.

The later repository-side diagram remains responsible for explaining that GAMK generates `AGENTS.md` and supplies the reusable `global/` source linked by consumers.

## Verification

- `scripts/test_install.py`: 42 tests passed.
- `scripts/test_finish_worktree.py`: 4 tests passed.
- `scripts/test_powershell_wrappers.py`: all probes passed.
- `scripts/generate_mother_agents.py --check`: current.
- Shell syntax and `git diff --check`: passed.

## Next

Integrate this review gallery into `main` and publish it. The user will then choose the project-side rendering to keep in a follow-up edit.
