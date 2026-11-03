---
work: 20261103_0030_wiki-before-decisions
branch: main
worktree: .
origin: user conversation
---

# Put wiki before decisions

The shared memory map now presents `wiki/` before `decisions/`. The canonical consumer template was updated first, the root `AGENTS.md` was regenerated, and the README's Mermaid map, directory list, and repository tree were aligned. The installer parity test was updated to assert the new section order.

Verification:

- `scripts/generate_mother_agents.py --check` passed.
- `scripts/test_install.py`: 42 tests passed.
- `git diff --check` passed.
