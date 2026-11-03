---
status: done
branch: feat/git-ai-global-mother
worktree: .git-worktrees/git-ai-global-mother
origin: user conversation
---

# Make ai-memory the git-ai-global mother repository

## Reopened scope (2026-11-02)

User clarified the intended AGENTS architecture: the consumer template is the common source; a deterministic generator will compose the mother repository's root `AGENTS.md` from that template plus mother-only extensions. A mother-only workflow (not a rule) will require running the generator when updating mother/template instructions. This supersedes the prior byte-identical-copy interpretation and requires regeneration/tests and synchronized memory before reclosing.

## Objective

Evolve this repository into the canonical source and installer for its existing `.ai/` structure, using `/home/marcosrdac/prj/git-ai-global` as implementation reference while preserving the current structure and user-approved decisions.

## Plan

1. Record confirmed architecture and installer decisions; inspect the legacy installer and current structure deeply enough to define a safe migration path.
2. Recreate the current `.ai/` directory layout in this worktree and establish the canonical `global/` source plus the versioned relative `.ai/global -> ../global` symlink for this mother repository.
3. Keep the root `AGENTS.md` and consumer template aligned by default, with explicit guidance for intentional mother-repository-specific changes.
4. Port and adapt the legacy installer: conservative read-only planning, preflight conflict detection before any writes, noninteractive install only when safe, local absolute global link for consumers, and a repair-link command.
5. Add consumer provenance manifest (source URL, full base commit, structural schema/version; no machine-specific absolute paths), global upgrade skill that asks the user about each structural change, and tests/documentation.
6. Add backlog items to study Git submodule distribution and a status/warning mechanism for source-vs-installed divergence.
7. Validate Linux behavior in this implementation task. Track actual Windows behavior separately; do not claim Windows support until PowerShell and symlink/junction behavior have been tested on Windows.

## Confirmed decisions

- Preserve the existing repository structure; `global/` at repository root is canonical.
- This repository itself has a tracked relative symlink `.ai/global -> ../global`; consumer links are local, absolute, ignored by the consumer Git, and repairable.
- `plan` is read-only and prints a contextual migration prompt with absolute target paths and the source commit. `install` preflights all relevant signals before writing; if any migration signal exists, it fails nonzero, lists findings, and points to `plan` without partial installation.
- Safe install with no relevant signals needs no `-y`; `-y` may remain available for automation but does not bypass conflict checks.
- Existing target `AGENTS.md` is integrated by the target project's agent, not overwritten by the installer. Prompt includes source commit and asks the agent to preserve legacy context/residue.
- Installer never edits a consumer's `.gitignore`, `.git/info/exclude`, or Git index. It warns the user to ignore the local absolute `.ai/global` link before committing; the mother repo's relative link is tracked normally.
- Record source URL, full source commit, and structural schema/version in a manifest under consumer `.ai/`; do not store local absolute paths there.
- Global upgrade skill uses diffs as evidence, compares against actual consumer state, explains consequences/negative tradeoffs per structural change, and gets the user's approval before each change. Never perform blind/automatic structural upgrades.
- Bring over most useful legacy behavior, including Bash/PowerShell wrappers and Windows support, subject to real validation.
- Keep root `AGENTS.md` aligned with the consumer template unless the user explicitly approves a mother-only difference; create guidance/skill for maintaining that parity.
- Backlog: investigate Git submodule distribution; investigate warning/status for divergence between installed base commit and available global source.
- User clarification (2026-11-02): `global/templates/project/AGENTS.md` is the source for shared instructions. Generate the mother root `AGENTS.md` from that template plus explicitly separate mother-only additions; do not duplicate shared instruction text by hand. A workflow local to this mother repository (not a rule and not installed to consumers) documents that agents must run the generator when updating the template or mother additions. The generator is not part of routine installer execution; run it only for AGENTS updates.

## Progress

- [x] Audit differences from the initial root AGENTS and classify them.
- [x] Remove accidental memory-structure additions and duplicated instruction sections.
- [x] Verify consumer/mother separation and local workflow behavior.
- [x] Verify generator reproducibility, `--check` no-write behavior, 33 tests, and static checks.
- [x] Windows validation remains a separate deferred task in `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.
- [x] Implement template-based mother AGENTS generator, mother-only extension source, and local workflow; add regression tests.
- [x] User-approved root/consumer shared instructions for `.ai/global/` discovery whether it is a directory or symlink.
- [x] Added Windows validation as a separate task in `work/next/` so it remains visible without blocking this Linux implementation task.
- [x] Final Linux verification: 30 tests, Python compilation, Bash syntax, parity check, relative-link check, and `git diff --check` pass.
- [x] Confirm current directory was not a Git repository and `.ai/work/` contained no tasks.
- [x] With explicit user authorization, initialize Git in the current project directory and commit `AGENTS.md` as the base commit (`40c317c997ecf6ca4bdc86155945c1e890ef8f4d`).
- [x] Create isolated branch `feat/git-ai-global-mother` and worktree `.git-worktrees/git-ai-global-mother`.
- [x] Inspect legacy repository commit (`a68495dc05e081c842fe00b55b9280d9621c667f`) and confirm its pre-existing `AGENTS.md` modification remains untouched.
- [x] Create this task record and reconstruct empty `.ai/` directories in the worktree.
- [x] Record detailed decisions, backlog entries, and progress log.
- [x] Complete Linux code review and verify behavioral consistency of modes/preflight.
- [x] Create a separate `next/` task for PowerShell wrappers and Windows symlink/junction validation.
- [x] Add deterministic AGENTS generation from consumer template + mother-only extensions, and document the mother-only update workflow.
- [x] Complete generator tests for deterministic output, single shared content, mother-only extensions, and read-only stale check.
- [x] Complete final documentation synchronization and full Linux verification.

## Relevant history and constraints

- The legacy repository is `/home/marcosrdac/prj/git-ai-global`, branch `main`, HEAD `a68495dc05e081c842fe00b55b9280d9621c667f`.
- Its `AGENTS.md` had a pre-existing user modification before this work. Do not edit/revert it or use the legacy worktree for implementation unless explicitly asked.
- The legacy suite passed all 14 tests when run using `nix shell nixpkgs#python3`.
- The user explicitly authorized initializing Git in `/home/marcosrdac/prj/ai-memory`; the sibling `/home/marcosrdac/prj/ai-memory-instance` remains untouched.
- Git does not track empty directories, so `.ai/` directories must be recreated as part of this branch.

## Reopened for final AGENTS audit (2026-11-02)

User asked to reopen this task and explicitly track remaining verification. Do not assume prior Linux tests establish that all changes to the original AGENTS instructions are intended. Compare current generated root with the initial committed AGENTS, shared template, and mother extension; classify differences and report/correct accidental changes under the user-approved structure.

No commit, merge, or push was requested or performed. The feature branch remains isolated and uncommitted.

## Associated analysis

- `.ai/analyses/doing/20261102_2005_installer-migration-design/README.md`

## Next action

No further Linux implementation action remains for this task. Keep native Windows validation deferred in `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`; do not commit, merge, or push without an explicit request.

## Progress update

### Handoff state (2026-11-02)

- **Current checkout:** branch `feat/git-ai-global-mother`, worktree `.git-worktrees/git-ai-global-mother`; HEAD remains base commit `40c317c997ecf6ca4bdc86155945c1e890ef8f4d`. All implementation is uncommitted and confined to this worktree. No merge/push has occurred.
- **AGENTS authorization:** user accepted the root skill/rule index entries after confirming they are isolated to this feature worktree, and later explicitly approved aligning the root instructions with the consumer template. The main worktree remains untouched.
- **Current files:** root `AGENTS.md`; `global/` source and consumer template; `scripts/install.py`, Bash/PowerShell wrappers, Python-free Bash/PowerShell copy installers, and `scripts/test_install.py`; `.ai/` tasks/decisions/analysis/log/wiki. Mother link is `.ai/global -> ../global` and resolves to `global/`.
- **Product paths:** Python installer is the migration-aware planner/installer/link repair; `copy-install.sh` and `copy-install.ps1` are deliberately limited no-Python bootstrap for an empty/new project. README documents boundaries.
- **Recent safety fixes:** `plan-mother` and `init-mother` are now read-only validators; neither creates or changes the source checkout's tracked link. Both fail if it is missing/wrong. Global-only install blocks occupied destinations and accepts only a destination resolving to this source's `global/`. Duplicate idempotency logic removed.
- **Template review:** user approved a template-source/generator model. Shared operating instructions cover `.ai/global/` as directory or symlink and follow its index. Mother-only instructions are in `.ai/templates/mother-AGENTS.extensions.md`, not `global/`; the workflow is in `.ai/workflows/`.
- **Latest verification (2026-11-02):** 33 tests pass after adding generator coverage. The generator writes root AGENTS from the consumer template plus mother extension; `--check` detects stale output without writing. Python compilation, generator `--check`, Bash syntax, `git diff --check`, and relative mother-link check pass.
- **Final verification:** reran generator `--check`, full 33-test suite, Bash syntax checks, and `git diff --check`; all pass. Windows tests are explicitly deferred to the separate next task.
- **Final AGENTS audit:** compared the generated root against the initial commit and classified the differences. The `.ai/global` discovery contract, project-local instruction discovery, index changes, and generated mother appendix are approved architecture; no unapproved `.ai/memory` path was present. Removed one accidental duplicate `Project instructions` section from the consumer template, regenerated the root file, and removed a duplicate test definition that had been shadowing coverage. Added a regression assertion that the shared section occurs exactly once.
- **Final audit verification:** generated composition matches the template plus mother extension exactly; root and consumer each contain one `Project instructions` section; consumer output contains no mother-only extension; `AGENTS.md --check`, 33 regression tests, Python compilation, Bash syntax, relative-link validation, and `git diff --check` pass.
- **Windows status:** Linux only. Windows PowerShell forwarding, symlink creation, and junction fallback have not been run; these are tracked in `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.
- **Git status at latest handoff:** modified root `AGENTS.md`; untracked `.ai/`, `README.md`, `global/`, and `scripts/`; no changes in legacy repo or sibling consumer. No commit or integration performed.

### Implementation summary and process correction

- Recreated the original `.ai/` structure with `.gitkeep` placeholders where Git would otherwise omit empty directories; added decisions, analysis, logs, wiki, and deferred tasks.
- Added canonical `global/`, templates, maintenance/context rules, and structural-upgrade guidance. Mother link is `.ai/global -> ../global` and is tracked as ordinary repository content.
- Implemented Python `plan`, `install`, `repair-link`, and read-only mother-link validation commands. Preflight blocks existing agent context and destination conflicts before writes; installation has rollback coverage and writes source provenance without local absolute paths.
- Added Python-free Bash and PowerShell copy-only bootstrap paths. They copy consumer `AGENTS.md` and create standard directories for clean projects, refuse common context signals, and do not claim migration/provenance/global-link functionality.
- User approved a generator architecture: shared instructions live once in the consumer template; root AGENTS is composed from that source plus separate mother-only extensions, including local rule loading and the mother-only update workflow.
- Installer never changes consumer ignore files or Git index; README warns users to ignore local `.ai/global` before committing. No root `.gitignore` was added.
- Exercised plan and blocked install against sibling `ai-memory-instance`; existing AGENTS and `.ai/` were reported, with no writes. The sibling is not a Git repository and was left unchanged.
- Earlier debugging found and fixed template duplication, CLI mode/preflight issues, unsafe mother-link mutation, and global-mode occupied-destination handling. The work/log maintenance failure and prevention are described in the associated kickoff log.

## Completion criteria

- The current structure is preserved and the repo is the canonical source for installation.
- Consumer AGENTS is canonical shared content; mother AGENTS is generated by the script from template plus mother-only extension, with no manually duplicated shared sections.
- The mother-only workflow precisely instructs agents when/how to run generation and is excluded from consumer installations.
- Planning/install/repair workflows are safe, preflight all target conflicts before writing, and include complete migration prompts.
- Provenance and structural upgrade guidance are documented and tested without automatic destructive changes.
- Linux behavior is covered by regression tests; platform claims accurately distinguish Linux/macOS implementation from Windows validation still pending.
- Consumer template is the canonical source for shared content. The generator composes root AGENTS with `.ai/templates/mother-AGENTS.extensions.md`, which tells agents to load local `.ai/rules/`, skills, and workflows. The mother-only workflow explains this regeneration procedure; these mother-specific files are outside `global/` and are not installed into consumers.
- Decisions, deferred backlog, Windows next task, wiki/documentation, logs, and task state accurately reflect implementation and unresolved platform validation.
