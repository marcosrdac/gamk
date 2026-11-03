---
work: 20261102_2248_reprioritize-native-windows
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Defer native Windows validation

The user decided that native Windows validation is useful but not a current priority. Its task was moved from `work/next/` to `work/pool/backlog/` as `20261102_2246_validate-native-windows-installers.md`.

The submodule distribution study (`010`) and source-divergence status design (`020`) remain in `work/next/`. The source-divergence task concerns how to warn when a consumer's recorded source commit/schema differs from the global source currently available, without treating intentional consumer customization as corruption or performing automatic upgrades.
