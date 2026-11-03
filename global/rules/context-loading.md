# Context Loading Protocol

The project's root `AGENTS.md` is the automatically discovered shared entry point. If `.ai/global/` exists as either a directory or symlink, read its `INDEX.md` when present and follow every “Always Read” entry. Also load relevant available `rules/`, `skills/`, and `workflows/`, including mandatory rules applying to the task. Do not assume every category exists. A consumer project must remain usable when `.ai/global/` is absent, dangling, or unreadable.

Keep reusable personal defaults under the mother repository's `global/`, and project-specific context under the consumer's `.ai/`. Do not recursively read `.ai/`; follow the root `AGENTS.md` context map and load only relevant documents. Explicit task instructions take precedence over project context, which takes precedence over personal global defaults.
