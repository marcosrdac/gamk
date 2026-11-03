---
status: done
origin: user conversation
branch: main
worktree: .
---

# Simplify the README memory diagram

## Objective

Keep the selected responsibility-map style as the README's single project-side Mermaid diagram, remove space-consuming descriptions, arrange the memory folders vertically, and show the optional `global/` layer last with a dashed border.

## Plan

1. Replace the three-option gallery with one compact responsibility map.
2. Preserve the `AGENTS.md` entrypoint and the documented project-memory order while placing the optional global source last as a visually separate link.
3. Check the README, commit directly on `main`, and push it for user review.

## Progress

- [x] Replace the gallery with the compact selected diagram.
- [x] Verify Markdown/Mermaid text and repository status.
- [x] Commit and push directly to `main`.

## Relevant history and decisions

- The user selected the visual style of the former Option C.
- The user explicitly authorized direct edits and pushes to `main` for this README-only iteration.
- `global/` should be the last visual node and should use a dashed border to signal its optional/linked nature.

## Completion criteria

- [x] README contains one compact project-side Mermaid diagram.
- [x] Folder labels have no explanatory descriptions inside nodes.
- [x] The diagram is vertically distributed where Mermaid permits.
- [x] `global/` is last and visually dashed.
- [x] `main` is pushed and clean.

## Next action

The compact diagram is ready for visual review in the published README.
