## Mother repository extensions

These instructions apply only to the canonical GAMK source repository. They are generated into the repository-root `AGENTS.md` and are never installed into consumer projects.

### Load mother-specific operating context

At startup, after the shared project context map:

1. Read `.ai/global/INDEX.md` and follow its **Always Read** entries.
2. Read every applicable mother-local rule in `.ai/rules/` before acting in its domain. These are repository-specific instructions; do not treat them as consumer defaults or copy them into the consumer template.
3. Follow relevant mother-local workflows in `.ai/workflows/`, then consult mother-local skills in `.ai/skills/` when they can improve the work.
4. Keep consumer-shared context in `.ai/templates/project/` and mother-only instructions in `.ai/`. Do not duplicate shared text in these extensions.

### Maintain generated agent instructions

When changing the shared consumer instructions or these mother-only extensions, follow the mother-local workflow `update-agent-instructions.md`. The consumer template is the source for shared content; regenerate the root `AGENTS.md` with the provided generator. Do not hand-edit generated root content.

### Finish completed worktrees

After a completed feature is integrated into `main`, follow `.ai/workflows/20261102_2321_finish-completed-worktree.md`. Run its dry-run checks from `main`, then apply cleanup only when the target worktree is clean, has no active `.ai/work/doing/` task, and its branch is already merged. Never use force removal or force branch deletion to bypass an unresolved condition.
