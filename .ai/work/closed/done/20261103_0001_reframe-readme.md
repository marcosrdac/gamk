---
status: done
origin: user conversation
branch: feat/readme-reframe
worktree: .git-worktrees/readme-reframe
---

# Reframe README around value, adoption, usage, and maintenance

## Objective

Rewrite `README.md` so it first sells the benefits of durable agent memory, then clearly explains that GAMK installs the memory system into other projects, then teaches practical usage, and finally documents GAMK's own structure and maintenance.

## Requirements

- Lead with the problem and the outcome before implementation details.
- Explain the agent-facing benefits quickly and convincingly.
- Make the source-repository/consumer-project relationship explicit.
- Provide a short path from zero to a safe installation in another project.
- Keep detailed commands, modes, safety, migration, provenance, tests, and platform limits.
- Explain how this repository itself is organized and maintained.
- Use a Mermaid flow when it makes the source-to-consumer relationship clearer.
- Avoid claiming native Windows validation that has not happened.

## Plan

1. Reorganize the README into: value proposition, how installation works, quick usage, operational reference, repository internals, and maintenance.
2. Keep commands and safety guarantees synchronized with the implementation.
3. Use one Mermaid diagram for the source-to-consumer relationship and keep file trees as text.
4. Run documentation/static checks and the relevant regression suites.
5. Close the task, integrate directly into `main`, and remove the temporary worktree with the lifecycle helper.

## Completion criteria

- [x] The first screen communicates the value and audience clearly.
- [x] The README explicitly explains installing GAMK into another project.
- [x] Practical usage appears before internal maintenance details.
- [x] Repository structure and maintenance are documented at the end.
- [x] Existing command and safety claims remain accurate.
- [x] A Mermaid flow clarifies the source-to-consumer relationship.
- [x] Checks pass and the task/worktree lifecycle is ready to complete.

## Progress

- [x] Drafted the value-first README structure.
- [x] Added the GAMK-to-consumer Mermaid flow.
- [x] Verified the README against the installer commands and current safety behavior.
- [x] Ran 42 installer tests, 4 cleanup-helper tests, PowerShell/NixOS probes, generator checks, and static checks.

## Next action

No implementation action remains; commit `1d3ea1f` was integrated into `main`, the temporary worktree was removed safely, and the updated `main` is ready for publication.
