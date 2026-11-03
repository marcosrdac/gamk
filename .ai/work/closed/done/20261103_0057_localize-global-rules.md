---
status: done
origin: user conversation
branch: feat/localize-global-maintenance
worktree: .git-worktrees/localize-global-rules
---

# Localize GAMK maintenance rules

## Objective

Separate optional reusable global context from rules that belong only to the GAMK source repository.

## Plan

1. Remove the duplicated context-loading rule from `global/`.
2. Move GAMK maintenance guidance into `.ai/rules/` and index local rules.
3. Update the mother extension, generated root instructions, README, wiki, and regression tests.
4. Validate generation, tests, syntax, and documentation consistency.

## Progress

- [x] Created an isolated worktree from `main`.
- [x] Confirmed that the installed `AGENTS.md` already defines the context-loading protocol.
- [x] Removed both global rules and moved GAMK maintenance guidance into `.ai/rules/20261103_0057_gamk-maintenance.md`.
- [x] Added `.ai/rules/INDEX.md`, updated the global index, mother extension, generated root instructions, README, wiki, tests, decision, and log.
- [x] Passed the generator, generator check, 42 installer tests, Bash syntax checks, and `git diff --check`.

## Relevant decisions

- Global context is optional personal context and must not impose GAMK-specific maintenance instructions on consumer projects.
- The consumer `AGENTS.md` remains the authoritative source for how context is discovered.

## Next action

Integrate this completed branch into `main`, push it, and clean the worktree.

## Completion criteria

- [x] No GAMK-specific maintenance or duplicated context-loading rule remains under `global/`.
- [x] Local GAMK rules are indexed and the mother extension is accurate.
- [x] Generated `AGENTS.md` is current and consumer instructions remain free of mother-only filenames.
- [x] Relevant tests and consistency checks pass.
