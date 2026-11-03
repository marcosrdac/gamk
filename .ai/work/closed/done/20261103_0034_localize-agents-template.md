---
status: done
origin: user conversation
branch: feat/local-agents-template
worktree: .git-worktrees/local-agents-template
---

# Localize the GAMK AGENTS template

## Objective

Move the canonical `AGENTS.md` template out of `global/` and into GAMK's mother-local `.ai/templates/` context so consumer repositories receive the generated `AGENTS.md`, not the source template as reusable global content.

## Plan

1. Move `global/templates/project/AGENTS.md` to `.ai/templates/project/AGENTS.md`.
2. Update the generator, installers, tests, rules, skills, workflows, wiki, `global/INDEX.md`, and README to use the new local source path.
3. Keep `global/` focused on reusable context and preserve consumer installation behavior: copy the generated template output as `AGENTS.md`, never copy the local source template.
4. Run generator/install/wrapper tests, review the source diff, merge to `main`, and clean this worktree.

## Progress

- [x] Move the template and update all path references.
- [x] Verify installer/generator behavior and documentation.
- [x] Commit, merge to `main`, and clean the worktree.

## Relevant history and decisions

- The user explicitly decided that the template is local to GAMK and should not be installed in consumer repositories.
- Root `AGENTS.md` remains generated; it must never be hand-edited.
- Consumer projects should continue receiving only their generated `AGENTS.md` and the reusable `global/` source through `.ai/global`.

## Completion criteria

- [x] No current operational reference treats `global/templates/project/AGENTS.md` as the canonical source.
- [x] The local template generates the root `AGENTS.md` and supplies installer output.
- [x] Consumer installation does not copy the local template into a target.
- [x] Relevant tests pass and the worktree lifecycle is complete.

## Next action

The local-template migration is ready to integrate; the analyses worktree will continue from the resulting `main` commit.
