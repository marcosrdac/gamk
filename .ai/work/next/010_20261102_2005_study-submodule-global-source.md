---
status: planned
origin: user conversation
---

# Study Git submodule distribution for global context

## Objective

Compare the current local absolute symlink model with including this mother repository (or a smaller source repository) as a Git submodule in consumers.

## Questions

- Does a submodule materially improve portability and reproducibility across machines?
- What user and agent workflows are required to add, clone, initialize, update, and repair it?
- How does it interact with consumer commits, private repository access, nested worktrees, and Windows?
- Could a smaller dedicated content repository avoid bringing installer and project history into every consumer?
- What are the security, maintenance, and contributor-experience tradeoffs?

## Current decision/context

The confirmed current direction is a local, unversioned absolute symlink in each consumer, repairable from the mother checkout. Do not change that direction without user approval. Findings should inform a later decision, not implement a submodule migration.

## Next action

After core installer behavior is working, conduct a documented comparison and recommend whether the submodule option should remain deferred.

## Completion criteria

- Evidence-based comparison covers portability, user workflow, update behavior, security/access, Windows, and impact on consumer Git state.
- A recommendation and unresolved questions are recorded; implementation remains out of scope unless separately approved.
