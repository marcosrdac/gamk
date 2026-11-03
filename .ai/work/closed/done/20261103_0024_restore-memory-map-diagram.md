---
status: done
origin: user conversation
branch: main
worktree: .
---

# Restore the README memory-map diagram

## Objective

Make the README diagram visibly match the responsibility-map model: `AGENTS.md` points into `.ai/`, and `.ai/` points to each memory area individually. Keep the areas vertically ordered, with the optional `global/` node last and dashed.

## Plan

1. Replace the sequential chain with direct `.ai/` edges to every memory area.
2. Use invisible ordering links to keep the map vertical without adding descriptions to nodes.
3. Verify the Markdown and publish directly to `main`.

## Progress

- [x] Replaced the sequential chain with direct `.ai/` edges.
- [x] Added vertical ordering links and a dashed final `global/` node.
- [x] Verify, commit, and push the README correction.

## Relevant history and decisions

- The user confirmed the former Option C visual language, not the sequential reading path.
- The user wants compact folder-only labels and direct GitHub review from `main`.

## Completion criteria

- [x] `AGENTS.md` points to `.ai/`.
- [x] `.ai/` points to each memory area individually.
- [x] `global/` is last and dashed.
- [x] `main` is pushed and clean.

## Next action

The responsibility-map correction is published; the next README review can confirm the vertical rendering.
