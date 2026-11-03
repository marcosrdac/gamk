---
work: 20261103_0041_analyses-before-decisions
branch: feat/analyses-before-decisions
worktree: .git-worktrees/analyses-before-decisions
origin: user conversation
---

# Put analyses before decisions

The shared memory tree, numbered AGENTS sections, README Mermaid diagram, README directory list, and parity test now present `analyses/` before `decisions/`.

Verification:

- `scripts/generate_mother_agents.py --check` passed.
- `scripts/test_install.py`: 42 tests passed.
- Bash syntax and `git diff --check` passed.
