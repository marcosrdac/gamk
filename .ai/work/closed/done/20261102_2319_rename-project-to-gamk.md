---
status: done
origin: user conversation
branch: feat/gamk-rename
worktree: .git-worktrees/gamk-rename
---

# Rename the project to GAMK and rewrite the README

## Objective

Rename the project's public identity from `git-ai-global` to **GAMK — Git Agent Memory Kit**, while preserving safe operation for existing consumers and producing a complete, newcomer-friendly `README.md`.

## Scope

- Update current public-facing names in source, templates, generated instructions, documentation, tests, and manifest identifiers.
- Preserve `.ai/`, script names, `.git-worktrees/`, and existing local paths as stable operational interfaces.
- Accept legacy `git-ai-global` manifest identifiers so already-installed consumers do not become unreadable after the rename.
- Document installation, operating modes, status checks, safety model, migration boundaries, testing, and platform limits in the README.
- Keep historical logs and closed task names as historical records unless a current pointer must be corrected.

## Related instructions and artifacts

- `.ai/skills/20261102_2005_agents-parity.md`
- `.ai/workflows/20261102_2200_update-agent-instructions.md`
- `.ai/rules/20261102_2005_agents-parity.md`
- `.ai/rules/20261102_2005_structural-upgrade.md`
- `.ai/workflows/20261102_2321_finish-completed-worktree.md`
- `.ai/decisions/20261102_2324_gamk-name.md`
- `.ai/decisions/20261102_2324_worktree-lifecycle.md`
- `.ai/logs/20261102_2324_gamk-rename-and-worktree-lifecycle.md`

## Plan

1. Define the public/internal naming boundary and compatibility behavior.
2. Update source manifest identifiers, installer validation/output, tests, templates, and current documentation.
3. Regenerate root `AGENTS.md` and verify mother/consumer parity.
4. Rewrite README as the canonical project introduction and operational guide.
5. Run the complete test and static-validation suite, close the task, and fast-forward directly into `main`.

## Completion criteria

- [x] Public identity consistently presents GAMK — Git Agent Memory Kit.
- [x] New source/consumer manifest identifiers work, while legacy identifiers remain readable.
- [x] README is complete enough for a new user to understand the project and use it safely.
- [x] Generated instructions, tests, wiki, and current pointers are synchronized.
- [x] Shared AGENTS worktree-lifecycle rule and mother cleanup workflow/helper are implemented.
- [x] Full tests, generator checks, wrapper probes, and diff checks pass.
- [x] Task is closed before direct integration into `main`.

## Next action

No implementation action remains; integrate this completed branch directly into `main`, then run the cleanup workflow from `main`.

## Progress

- [x] Renamed current public identity and manifest identifiers to GAMK, preserving legacy reads.
- [x] Rewrote the README as the project entrypoint and operational guide.
- [x] Added the shared worktree lifecycle rule to the consumer template.
- [x] Added the mother-only cleanup helper, workflow, tests, and dry-run/refusal checks.
- [x] Ran 42 installer tests, 4 cleanup-helper tests, PowerShell/NixOS probes, generator checks, and static checks.
