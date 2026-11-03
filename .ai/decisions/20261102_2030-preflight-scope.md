# Decision: preflight before consumer installation

- **Status:** Confirmed interpretation for implementation; detailed detector remains testable and revisable.
- **Originating work:** `010_20261102_2005_git-ai-global-mother.md`.
- **Analysis:** `../analyses/doing/20261102_2005_installer-migration-design/README.md`.
- **Origin:** User conversation on 2026-11-02.

## Decision

An installer may proceed without `-y` only when a complete read-only preflight finds no relevant migration signal. Any detected relevant signal blocks full `install` before the first consumer mutation, returns a nonzero status, lists the signals, and points to `plan` for a contextual agent migration prompt. `-y` never bypasses this safety gate. Link-only operations inspect the link destination and do not rewrite or assess project context.

“Relevant signal” for full structure installation means evidence that project instructions/context already exist or that a planned destination is occupied: root/nested `AGENTS.md`; known agent instruction/configuration files; existing `.ai/` tree; or occupied generated-file/link destinations. Detection is conservative and reports evidence, not a claim that the existing project is incompatible. Ordinary unrelated source files alone are not a conflict. `local` and `global` modes examine only destinations they will write.

## Rationale

The user explicitly requires detecting conflicts before acting and forbids discovering a problem after installation has started. Treating every nonempty repository as a conflict would make direct installation unusable, so signals must be scoped to instruction/context and destination paths while remaining broad across known conventions.

## Consequences

- Preflight must be pure/read-only, including not creating `.ai/`, ignore files, or temporary files in the consumer.
- Tests must snapshot consumer filesystem state and prove exact non-mutation on every blocking condition.
- `plan` should be useful even when it reports no signals, but its migration prompt is most important when findings exist.
- The catalog of known instruction/configuration paths should be documented and tested; unknown conventions remain a limitation, so the prompt should ask the target agent to inspect its own repository context.
