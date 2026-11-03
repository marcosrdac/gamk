---
status: done
origin: user conversation
branch: main
worktree: .
---

# Show GAMK as the source of the installed structure

## Objective

Add a compact source-side explanation without changing the current project-side diagram: GAMK generates `AGENTS.md` and `.ai/`, and `global/` is linked into `.ai/global`.

## Plan

1. Keep the current horizontal project-memory diagram unchanged.
2. Add a small Mermaid source diagram and one explanatory sentence.
3. Render, verify, and publish directly to `main`.

## Progress

- [x] Added the source-side Mermaid diagram.
- [x] Added the concise explanation of the `.ai/global` link.
- [x] Verify, close, commit, and push.

## Relevant history and decisions

- The user wants the current folder layout preserved while making the repository's generator role explicit.
- `global/` is a source directory; consumers receive a local `.ai/global` link to it.

## Completion criteria

- [x] The existing project-side diagram remains structurally unchanged.
- [x] The README shows GAMK generating `AGENTS.md` and `.ai/`.
- [x] The README shows `global/` linked through `.ai/global`.
- [x] `main` is pushed and clean.

## Next action

The source-side diagram is published alongside the unchanged project-side diagram.
