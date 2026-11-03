# Agent-led structural upgrade for consumer projects

## Purpose

Guide a deliberate upgrade of an installed `.ai/` structure using this repository's source history, without blindly replacing consumer-maintained context.

## Inputs to inspect

1. Consumer root `AGENTS.md` and all project instruction/configuration files relevant to the change.
2. Consumer `.ai/` context map, pending work, decisions, rules, current memory, and any legacy/archived structures implicated by the proposed change.
3. Consumer `.ai/<manifest>` provenance: source URL, installed base commit, and structural schema/version.
4. The mother repository's current `global/templates/project/` and the source history/diff from the recorded base commit to the candidate commit. Do not infer a local absolute path from the manifest; use the available `.ai/global` link, a configured checkout, or the recorded Git URL as appropriate.
5. Actual consumer files and Git status; distinguish committed, modified, ignored, and untracked user data.

## Method

- Treat the source diff as evidence of what changed in the canonical template, not as an instruction to copy or overwrite.
- Compare three states conceptually: the old structure represented by the recorded base, the consumer's current state, and the proposed new structure.
- Identify each discrete structural or instruction change, affected consumer paths, dependencies, and any legacy material that may need careful agent-assisted reconstruction.
- For each proposed change, state: intended benefit, what would change, compatibility assumptions, work needed to adapt/rebuild existing context, risks or negative tradeoffs of adopting it, and risks of declining it.
- Ask the user whether to accept, reject, or defer each change. Do not apply undecided changes. A change that has multiple independent consequences should be split into separate decisions.
- After approval, adapt consumer files in place while preserving useful legacy behavior and provenance. Never replace an entire `.ai/` tree or `AGENTS.md` merely to match the current template.
- Keep the consumer manifest's installed base commit/schema accurate only after the user-approved migration is actually complete. If only part is adopted, document partial state instead of claiming the consumer is fully upgraded.
- Run relevant project tests/validation and report remaining differences, deferred decisions, and any residual legacy paths.

## Safety boundaries

- No automatic structural upgrade.
- No destructive cleanup of legacy files or directories without explicit, item-specific user approval.
- No machine-specific absolute paths in versioned manifest/documentation.
- Do not mark the consumer as fully migrated while approved work remains incomplete.

## Output

Provide a concise per-change decision table (accepted/rejected/deferred), affected paths, rationale, validation, and exact remaining work. Update the consumer's root `AGENTS.md` context map and current memory when the resulting structure changes.
