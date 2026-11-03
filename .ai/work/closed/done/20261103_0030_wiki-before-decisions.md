---
status: done
origin: user conversation
branch: main
worktree: .
---

# Put wiki before decisions

## Objective

Make `wiki/` appear before `decisions/` in the shared `AGENTS.md` memory map and the README's corresponding diagrams, lists, and repository tree.

## Plan

1. Update the canonical consumer template, including its memory tree and numbered sections.
2. Regenerate the root `AGENTS.md` and update the README's matching order references.
3. Run generator checks and relevant regression tests, then publish directly to `main`.

## Progress

- [x] Update the canonical template and README order.
- [x] Regenerate and verify root `AGENTS.md`.
- [x] Run checks, close, commit, and push.

## Relevant history and decisions

- The user explicitly chose `wiki/` before `decisions/` as the preferred knowledge-flow order.
- The consumer template remains canonical; root `AGENTS.md` must be regenerated rather than hand-edited.

## Completion criteria

- [x] The `.ai/` tree places `wiki/` before `decisions/`.
- [x] The numbered instruction sections present Wiki before Decisions.
- [x] README diagrams, lists, and repository tree match the order.
- [x] Generator checks and relevant tests pass; `main` is pushed and clean.

## Next action

The `wiki/`-before-`decisions/` order is published in the generated instructions and README.
