---
work: 20261103_0117_direct-global-index
branch: fix/direct-global-index
worktree: .git-worktrees/direct-global-index
origin: user conversation
---

# Make the global index agent-directed

`global/INDEX.md` was shortened and reframed as direct operational guidance for an agent already reading it from project context. It now tells the agent to use the index as a router, skip categories marked `empty`, open only task-relevant files, respect local/project precedence, and follow `Always Read` entries when present.

Distribution details about consumer projects, links, copying, and repository topology were removed from the index. Regression coverage preserves the category-status contract and rejects those terms from the index. The installer test suite (42 tests), generator freshness, and diff checks passed.

Next: integrate into `main`, push `origin/main`, and clean the temporary worktree.
