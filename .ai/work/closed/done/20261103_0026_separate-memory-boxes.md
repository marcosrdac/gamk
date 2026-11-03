---
status: done
origin: user conversation
branch: main
worktree: .
---

# Separate the horizontal README memory boxes

## Objective

Keep the horizontal `AGENTS.md` → `.ai/` → memory layout while restoring one separate box per memory folder inside the right-hand block.

## Plan

1. Use a right-hand Mermaid subgraph with vertically stacked folder nodes.
2. Keep the folder labels compact and `global/` last with a dashed border.
3. Render, verify, and publish directly to `main`.

## Progress

- [x] Replaced the single text node with separate folder nodes in a right-hand block.
- [x] Kept the horizontal relationship and vertical folder order.
- [x] Verify, close, commit, and push.

## Relevant history and decisions

- The user wants separate folder boxes but found the previous fan-out layout difficult to read.
- The intended composition is `AGENTS.md` on the left, `.ai/` in the middle, and the folder block on the right.

## Completion criteria

- [x] Folder boxes remain separate.
- [x] The right-hand block is vertically organized.
- [x] `main` is pushed and clean.

## Next action

The separate-box horizontal layout is published for visual review.
