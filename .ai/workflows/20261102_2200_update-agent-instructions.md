# Update mother agent instructions

This workflow is local to the canonical mother repository. It is not shipped to consumer projects.

## When to use

Run this workflow only when changing shared instructions in `.ai/templates/project/AGENTS.md` or mother-only additions in `.ai/templates/mother-AGENTS.extensions.md`. It is not part of routine installation or project task startup.

## Procedure

1. Read `.ai/rules/20261102_2005_agents-parity.md` and inspect the current consumer template and mother extensions.
2. Put common instructions in `.ai/templates/project/AGENTS.md`. Put instructions that apply only to this canonical source repository in `.ai/templates/mother-AGENTS.extensions.md`. Do not put mother-only instructions under `global/` or duplicate shared text in the extension.
3. Do not hand-edit the generated root `AGENTS.md`.
4. Run `python scripts/generate_mother_agents.py` from the repository root.
5. Run `python scripts/generate_mother_agents.py --check`; confirm it reports the root file is up to date.
6. Review the generated diff. Confirm shared text occurs once, mother-only content is only in root output, and no private path, credential, or mother-only filename leaked into the consumer template.
7. Run the relevant regression tests and `git diff --check`. Update task/log/wiki/decision records when the instructions' behavior or architecture changed.

## Safety

- The consumer template is authoritative for shared instruction text.
- Mother additions are explicit, separate, and generated as an appendix after shared content.
- The generator is not run automatically during install; it is run when agent instructions are deliberately updated.
- If the generator or template model changes, update its tests and this workflow in the same task.
