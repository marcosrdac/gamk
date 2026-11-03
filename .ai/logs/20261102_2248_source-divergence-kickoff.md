---
work: 20261102_2005_source-divergence-status
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Start source-divergence design

The user promoted the source-versus-installed divergence task from `work/next/` to `work/doing/`. Native Windows validation was left in the backlog because it is not currently prioritized; the submodule study remains the first queued task after this investigation.

The initial investigation documents the current `.ai/git-ai-global.json` fields and compares provenance filename options. The leading recommendation is `.ai/provenance.json`, but no filename or format change has been applied yet. The next work is to confirm the name, define low-noise status states, and design tests without enabling automatic upgrades.
