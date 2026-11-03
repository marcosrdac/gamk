---
status: done
origin: user conversation
branch: feat/revert-mermaid-entry-layout
worktree: .git-worktrees/revert-mermaid-entry-layout
---

# Revert the first Mermaid entry layout

## Objective

Restore the first README Mermaid to the simpler layout with `AGENTS.md` and
`.ai/` connected horizontally to the left of the larger memory box.

## Plan

1. Revert only the entrypoint layout and its associated task log.
2. Validate the README diff and close the task.
3. Integrate into `main`, push, and clean the worktree.

## Progress

- [x] Restore the previous Mermaid layout.
- [x] Validate, close, merge, push, and clean.

## Completion criteria

- [x] The first Mermaid is `AGENTS.md → .ai/ → memory structure`.
- [x] The `rules → workflows → skills` order remains unchanged.
- [x] No unrelated files are changed.

## Next action

The original first Mermaid layout is restored and ready to integrate.
