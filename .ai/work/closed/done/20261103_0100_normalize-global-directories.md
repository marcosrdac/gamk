---
status: done
origin: user conversation
branch: feat/normalize-global-directories
worktree: .git-worktrees/normalize-global-directories
---

# Normalize global context directories

## Objective

Keep the global context source's declared categories present so the `.ai/global` link exposes an understandable, navigable structure.

## Plan

1. Add versioned markers for the global `rules/`, `workflows/`, `skills/`, and `hosts/` directories.
2. Align the README and regression tests with the actual global tree.
3. Validate the repository, integrate into `main`, and then rename the main checkout directory from `ai-memory` to `gamk`.

## Progress

- [x] Confirmed that the shared `AGENTS.md` already reads `.ai/global/INDEX.md` when the optional link or directory exists.
- [x] Confirmed that old `ai-memory` references are historical records or an external test path, not active configuration.
- [x] Added versioned markers for all four global categories listed by `global/INDEX.md`.
- [x] Updated README and regression tests; 42 installer tests, Bash syntax checks, and `git diff --check` passed.

## Relevant decisions

- Global context is optional personal context; the directory categories provide destinations without imposing instructions.
- The local main checkout will be renamed from `ai-memory` to `gamk` after integration.

## Next action

Integrate into `main`, push, safely clean the feature worktree, and rename the main checkout directory.

## Completion criteria

- [x] The global source contains all categories documented by its index.
- [x] README and tests describe the real global tree.
- [ ] Changes are integrated and pushed to `main`.
- [ ] The local main checkout is renamed to `/home/marcosrdac/prj/gamk`.
