---
status: done
origin: user conversation
branch: main
worktree: .
---

# Make the README memory block horizontal

## Objective

Present `AGENTS.md`, `.ai/`, and the memory folders as a clear left-to-right relationship, with all folders inside one multiline text block.

## Plan

1. Replace the multi-node boxed graph with a single folder-list node.
2. Keep `AGENTS.md` on the left, `.ai/` in the middle, and the folder block on the right.
3. Verify Mermaid rendering and publish directly to `main`.

## Progress

- [x] Replaced the individual folder nodes with one multiline block.
- [x] Set the horizontal order to `AGENTS.md` → `.ai/` → folder block.
- [x] Verify, close, commit, and push.

## Relevant history and decisions

- The user found the individual folder boxes and arrows difficult to read.
- The user explicitly requested a single text block to the right of `.ai/`.

## Completion criteria

- [x] All folders appear in one block.
- [x] `global/` is the final line in that block.
- [x] `main` is pushed and clean.

## Next action

The horizontal single-block diagram is published for visual review.
