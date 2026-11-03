---
status: done
work: ../../../work/closed/done/20261102_2005_git-ai-global-mother.md
related_decision: ../../../decisions/20261102_2005_git-ai-global-mother-architecture.md
---

# Installer and migration design

## Objective

Translate the user-confirmed architecture into concrete, testable installer behavior, especially the meaning of relevant conflict signals and the guarantee that no write occurs before complete preflight.

## Method

- Compare the current mother repository's original structure and instructions with the legacy `git-ai-global` installer, template, tests, and README.
- Derive observable conservative signals and command responsibilities.
- Test preflight behavior using isolated temporary consumer repositories and assert their complete filesystem state remains unchanged on conflict.

## Progress

- [x] Read the current root `AGENTS.md` and legacy installer guidance, implementation, tests, and README during the preceding repository review.
- [x] Define exact command surface and target path resolution.
- [x] Define conflict signal catalog and prompt content.
- [x] Design transactional/write-order behavior and local ignore management.
- [x] Verify conclusions against expanded Linux tests and document remaining platform uncertainties.

## Findings

- The legacy implementation copies additive starter files, preserves existing templates, defaults to preserving existing `AGENTS.md`, and can optionally prepend a marked managed block. This project deliberately replaces that merge behavior for detected existing context with a read-only plan and target-agent-led migration.
- Legacy installer exposes `full`, `local`, and `global` modes; supports project root, `.ai/`, and exact `.ai/global` targets; has Bash/PowerShell wrappers and a 14-test regression suite.
- The legacy consumer template has a managed-block marker, which is not required for the mother/consumer template parity direction unless implementation proves it useful for a fresh target. Existing target AGENTS must be treated as a migration signal, not auto-modified.
- Legacy global link creation uses symlink on Unix, symlink then junction fallback on Windows; its installer edits consumer `.gitignore`, which is explicitly rejected here. The new installer must not edit `.gitignore`, `.git/info/exclude`, or Git index; it warns users to ignore `.ai/global` before committing. The mother repository tracks its own relative link normally.
- Current root AGENTS describes continuity structure; the legacy consumer template has extra `hosts` and `docs`, forms `archived`, and plan lifecycle directories. These are not automatically adopted: the existing `.ai/` structure remains authoritative unless the user later approves a structural change.
- Preflight covers known root/nested agent instructions, known agent-specific config locations, an existing `.ai/`, and actual generated-file/link destination collisions. Ordinary unrelated project files (for example README/source code) alone do not block installation; their semantics cannot be inferred by the installer.
- Read-only plan plus blocked install were exercised against `/home/marcosrdac/prj/ai-memory-instance`, which has pre-existing AGENTS and `.ai/` context. Plan printed absolute paths and the full source commit; install returned nonzero and made no changes. Git status could not be obtained because the sibling directory is not a Git repository.
- Current legacy checkout has pre-existing `AGENTS.md` modifications and is only a read-only source reference during this implementation.

## Evidence

- Legacy installer: `/home/marcosrdac/prj/git-ai-global/scripts/install.py`.
- Legacy tests: `/home/marcosrdac/prj/git-ai-global/scripts/test_install.py` (14 passing under Nix-provided Python 3).
- Legacy consumer context template: `/home/marcosrdac/prj/git-ai-global/global/templates/project/AGENTS.md`.
- Legacy README: `/home/marcosrdac/prj/git-ai-global/README.md`.
- Current mother baseline: commit `40c317c997ecf6ca4bdc86155945c1e890ef8f4d`.

## Uncertainties

- Exact list of supported agent configuration/instruction paths must be enumerated without relying on guesses about every tool.
- On Windows, junction creation/removal and PowerShell argument forwarding require an actual Windows runner; neither has been run here. Both the full PowerShell wrapper and Python-free `copy-install.ps1` remain unvalidated. Follow-up is tracked in `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md` because it is not currently prioritized.
- Handoff review added Linux regression coverage that `plan-mother`/`init-mother` do not create a missing source link and that global-only install refuses an occupied destination. AGENTS parity/global-loading tests were subsequently added; the complete Linux suite now passes 30 tests.
- User explicitly approved aligning root and consumer `AGENTS.md`. Their shared operating contract consumes `.ai/global/` whether a symlink or directory, follows `INDEX.md` “Always Read” entries, and loads relevant available `rules/`, `skills/`, and `workflows/`; global context remains optional for collaborators. Mother-only inventories are not embedded in the consumer template.
- User later clarified a generator architecture: consumer template is canonical shared content; mother root `AGENTS.md` is generated by appending a separate mother-only extension. A mother-only workflow (not a consumer rule) requires running generation on deliberate instruction updates, not during installs. The mother extension identifies local `.ai/rules/`, skills, and workflows.
- Generator verification: 33 Python regression tests pass, including deterministic generation, stale check refusal without writes, one shared template section, mother extension appended only to root, and mother-only workflow presence. Bash syntax, Python compilation, `git diff --check`, and generator `--check` pass on Linux.
- Git metadata for local ignored links must not assume the target has a `.git` directory; Git worktrees use a `.git` file.

## Next action

The base implementation had been closed at `.ai/work/closed/done/20261102_2005_git-ai-global-mother.md` and was reopened for generator work; current active record is now closed. Native Windows validation remains tracked in `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.
