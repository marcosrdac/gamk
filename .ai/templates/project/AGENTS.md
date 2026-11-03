# Agent Instructions

If this file is in your context, you have already received the repository's root `AGENTS.md`. These are your operating instructions; do not reread it unless modified.

**Your responsibility is to maintain project continuity across agents, sessions, and context resets.** Every activity must be tracked in `.ai/work/`. Preserve execution context, investigate existing knowledge, and keep the repository's memory current.

## 1. Workspace Isolation

**Never modify the main Git worktree unless explicitly instructed by the user.**

- Default: create a dedicated branch and worktree under `<repo>/.git-worktrees/`.
- If already inside an appropriate worktree, continue there.
- Inspect existing worktrees and branches before creating new ones. Never overwrite unrelated work.
- The main worktree may be inspected, but not modified by default.
- Record `branch` and `worktree` in the corresponding work task's YAML.
- Preserve branch, worktree, current task, progress, and next action in every context handoff or compaction.
- Before merging, verify completion, tests, and the work-state requirements below.

### Worktree lifecycle

A dedicated worktree is temporary execution space, not permanent project inventory. When its task is complete:

1. Close the task: move it to `work/closed/done/` or `work/closed/wontdo/`, leaving `work/doing/` empty.
2. Verify tests and integrate the branch into the project's approved base branch.
3. From a different clean checkout of that base branch, confirm all of the following before cleanup:
   - the current checkout is the approved base branch;
   - the target is a registered worktree below `.git-worktrees/`;
   - the target branch is already merged into the base branch;
   - the target has no uncommitted or untracked files;
   - the target's `.ai/work/doing/` has no active task files; and
   - the target is not the main worktree or a detached checkout.
4. From that base checkout, remove the completed worktree with `git worktree remove <path>` and delete only its already-merged branch with `git branch -d <branch>`.
5. Run `git worktree prune` to clear stale administrative records.

For the usual layout, the cleanup commands are:

```bash
git worktree remove .git-worktrees/<worktree-name>
git branch -d <branch>
git worktree prune
```

Never remove the current worktree, a dirty worktree, or an unmerged branch. Never use `git worktree remove --force` or `git branch -D` to bypass an unresolved condition. If cleanup is blocked, preserve the worktree and resolve the reported task, data, or integration issue explicitly.

## 2. Repository Memory — `.ai/`

```text
.ai/
├── work/             # Tasks, priorities, execution state
│   ├── doing/
│   ├── next/
│   ├── pool/
│   │   ├── blocked/
│   │   ├── backlog/
│   │   └── ideas/
│   └── closed/
│       ├── done/
│       └── wontdo/
├── logs/             # Chronological project journal
├── wiki/             # Living project knowledge base
├── analyses/        # Research, evidence, analysis
├── decisions/        # Significant decisions and rationale
│   ├── doing/
│   └── closed/
│       ├── done/
│       └── wontdo/
├── forms/            # Structured asynchronous user decisions
│   ├── creating/
│   ├── pending/
│   └── answered/
├── global/           # Optional shared context (directory or local symlink)
├── rules/            # Mandatory context-specific instructions
├── workflows/        # Repeatable operational procedures
├── skills/           # Specialized agent capabilities
└── templates/        # Document and artifact templates
```

**Discovery:** Treat `.ai/` as the repository's persistent memory. Explore directories using `ls`, `find`, `rg --files`, or equivalents. Use filename prefixes, sorting, and filtering for efficient navigation. Proactively inspect related files, follow references, and investigate dependencies, previous decisions, and documentation. When uncertain, expand the search rather than assume information is irrelevant. Never sacrifice understanding to reduce context consumption.

**Relationship:** `work/` tracks every activity; other directories contain associated artifacts, knowledge, or operational resources. Every analysis, form creation, documentation change, or other substantive activity must be tracked by a work task.

**Project instructions:** At startup, discover applicable project rules in `.ai/rules/` and read each rule relevant to the task before acting. Follow relevant workflows in `.ai/workflows/`, then consult project skills in `.ai/skills/` when they can improve the work. These project-local instructions are distinct from optional shared global context.

**Optional shared context:** At startup, attempt to read `.ai/global/INDEX.md` directly. If the link, file, or contents are absent or unreadable, continue without global context; do not first test for the path or scan other global directories. Treat the index as the catalog of available categories, follow its “Always Read” entries when present, and consume only categories relevant to the task. Do not assume every category exists. Global guidance is a personal default: explicit task instructions take precedence over project instructions, which take precedence over global context. Global context must not be required for collaborators.

## 3. Work Management

### Naming and ordering

- `work/doing/`, `work/next/`: `<ORDER>_<YYYYMMDD>_<HHMM>_<slug>.md`
- Other work directories: `<YYYYMMDD>_<HHMM>_<slug>.md`
- Timestamp = original creation time; immutable across moves.
- `ORDER` = ascending execution precedence, independent per directory.
- Start at `010`, `020`, `030`...; use gaps (`000`, `005`, `015`...) for insertions.
- No duplicate orders. Renumber only when necessary.
- Preserve timestamp and slug when moving; add/remove/reassign `ORDER` as appropriate.

### Task documents

Each task is a single Markdown file containing YAML frontmatter, objective, plan, progress, relevant history/decisions, next action, and completion criteria. Keep it accurate, current, and independently resumable.

```yaml
---
status: active
branch: feat/example
worktree: .git-worktrees/example
---
```

In `doing/`, use `status: active | paused`. For interruptions, record `paused_at` and `pause_reason`. For blockers, record `blocked_at`, `blocked_reason`, `unblock_condition`, and `previous_state`.

Reference associated analyses, forms, decisions, wiki pages, and logs. Use the timestamp and slug (without `ORDER`) as stable task references.

### Execution protocol

1. **Inspect `doing/` first.** Read task documents by ascending `ORDER`, reconstruct their context, and continue the active task unless the user's objective overrides it. If none is active, resume the lowest-order paused task. At most one task should be active per worktree.
2. **Completion:** verify criteria, update the task, move to `closed/done/`, remove `ORDER`, and resume the next paused task.
3. **Interruption:** checkpoint progress and next action, set `status: paused`, record reason/time, and insert the new active task ahead using a lower available `ORDER`. Preserve relative ordering. This supports last-paused-first-resumed by default.
4. **External blocker:** record dependency, unblock condition, and checkpoint; move to `pool/blocked/`. When resolved, return to `doing/` or `next/` according to context.
5. **Empty `doing/`:** promote the lowest-order task from `next/` to `doing/` as `010_...`, mark active, and execute.
6. **Both empty:** inspect `pool/backlog/` (concrete demands) and `pool/ideas/` (exploratory proposals); recommend candidates for `next/`. Do not promote without authorization.
7. **Abandonment:** record the reason and move to `closed/wontdo/`.

`next/` typically contains 0–5 tasks. Prefer finishing paused work before starting new tasks. Explicit user objectives override default scheduling, but never justify losing execution context.

**Git invariant:** `.ai/work/doing/` must be empty before merging a work branch into `dev`/`main`. Never move unfinished tasks merely to bypass this rule. Resolve partial changes from blocked or abandoned work before integration.

## 4. Logs

`logs/<YYYYMMDD>_<HHMM>_<slug>.md`

**`logs/` is the continuously maintained, human-readable project journal.** Anyone browsing recent logs should quickly understand what happened, what changed, current direction, difficulties encountered, and next steps.

Record meaningful events throughout work, not only upon completion:

- Progress, milestones, implementations, and verification results.
- Important discoveries, failures, blockers, and changes of direction.
- Significant decisions and their consequences.
- Analyses, forms, and wiki pages created or updated.
- Integrations, releases, and other relevant repository events.

Each log should explain **what happened, why it matters, and what comes next**, as applicable.

- Use YAML to reference the originating `work` task, branch, and worktree.
- If originating directly from a user conversation, record that origin explicitly, along with the corresponding work task.
- Create independent timestamped logs for distinct events; use unique slugs/suffixes to avoid collisions.
- Treat published logs as immutable except for factual corrections.
- Record significant progress during long-running tasks, including unresolved issues.
- Avoid command-by-command narration and duplication of detailed task history.
- Logs are branch-local until integrated; distinguish local progress from the integrated project state.

## 5. Wiki

`wiki/<slug>.md`

**`wiki/` is the living knowledge base and authoritative documentation of the repository.** It must enable agents and humans to understand the project without reconstructing its history.

- Proactively search and consult existing wiki pages before making assumptions or implementing consequential changes.
- Document architecture, behavior, concepts, interfaces, conventions, rationale, and established knowledge.
- Create or update wiki pages when requested or when work materially changes documented understanding.
- Keep pages coherent, navigable, and current; link implementation, decisions, and analyses.
- Investigate and correct outdated, contradictory, or unclear documentation.
- Prefer consolidated knowledge over chronological narration; history belongs in `logs/` and `decisions/`.
- Record meaningful documentation changes in `logs/`.

The wiki should describe **what is currently understood and why**, not merely what was done.

## 6. Analyses

Substantial research and analysis intended for both agents and human reading. Analyses are independent knowledge artifacts, but their execution is always tracked in `work/`.

```text
analyses/
├── doing/
│   └── YYYYMMDD_HHMM_slug/
│       ├── README.md       # Required entrypoint
│       └── ...             # Research, evidence, analyses, figures
└── closed/
    ├── done/
    └── wontdo/
```

- `README.md` controls the analysis's state and summarizes its objective, methodology, progress, findings, evidence, uncertainties, and next steps.
- YAML must identify `status`, originating `work` task, and relevant relationships.
- Use `status: active | paused` while in `doing/`; document interruptions.
- Organize supporting material freely, preserving navigability and traceability.
- Analyses may remain open, paused, or awaiting additional information.
- Close as `done` when the defined research scope is satisfied; use `wontdo` for abandoned analyses, explaining why.
- Separate evidence, interpretation, hypotheses, and unresolved questions.
- Link resulting forms, decisions, wiki pages, and logs.
- Transfer durable findings to `wiki/` when appropriate.

Analyses are designed for repeated consultation, including directly by the user. They must remain understandable independently of their originating task or conversation.

## 7. Decisions

`decisions/<YYYYMMDD>_<HHMM>_<slug>.md`

Record significant decisions arising from conversations, analyses, forms, or implementation.

Include the decision, context, rationale, alternatives considered, consequences, and origin.

- Distinguish confirmed decisions from proposals, preferences, and unresolved questions.
- Link originating work, analyses, forms, and relevant wiki pages.
- Record decisions that constrain product behavior, architecture, scope, or future work.
- Preserve historical decisions; explicitly reference superseded decisions rather than silently rewriting them.
- Update `wiki/` when decisions change the project's current understanding.
- Record significant decisions in `logs/`.

## 8. Forms

Forms enable **asynchronous, multi-question user decision-making without repeated conversational exchanges**. They are particularly useful when many interdependent operational choices require coherent user input.

Lifecycle:

`creating/ → pending/ → answered/`

Files: `<YYYYMMDD>_<HHMM>_<slug>.md`

### Creating

Creating a good form is substantive, often multi-stage work involving analysis, comparison, synthesis, and question design.

- Track form creation in `work/`, preserving progress across sessions.
- Research alternatives, implications, examples, and dependencies before finalizing questions.
- Consult originating analyses and relevant repository knowledge.
- Use available form templates and adapt them to the decision context.
- Record provenance in YAML: originating work, analyses, and/or user conversation. **If a form originates from an analysis, explicitly reference that analysis.**

### Form quality

**Each question must contain enough information for the user to make an informed decision independently.**

Provide, as appropriate:

- The precise decision being requested and why it matters.
- Available alternatives, including reasonable custom options.
- Concrete examples and realistic outcomes.
- Comparisons, trade-offs, advantages, disadvantages, and risks.
- Dependencies on previous answers or other decisions.
- Relevant evidence, justified recommendations, and implications.
- Space for free-form answers, uncertainty, deferral, or partial responses.

Avoid fragmented questions, unnecessary back-and-forth, or requiring the user to research information the agent could have supplied.

### Pending and answered

- When the form is complete and ready for user input, move it from `creating/` to `pending/`.
- **Immediately tell the user that the form is ready, provide its location, and explicitly request that they answer it.**
- The user may answer asynchronously, incrementally, and only as extensively as desired.
- Keep the form in `pending/` until the user indicates that they have finished; never equate unanswered questions with rejection or implicit choices.
- When finished, preserve all responses and move the form to `answered/`.
- Resume related work, record significant confirmed decisions in `decisions/`, and update the wiki when appropriate.

A pending form may remain pending indefinitely without blocking unrelated work. Its originating task may be completed or blocked according to its actual completion criteria.

## 9. Rules

`rules/<YYYYMMDD>_<HHMM>_<slug>.md`

Rules contain mandatory context-specific instructions.

- **Read every applicable rule before acting in its domain.**
- Use the project/global indexes and directory listings to identify applicability; investigate further whenever scope is uncertain.
- Maintain a complete project-local rules index in `.ai/` documentation containing each filename and a brief scope. Global rules are indexed by `.ai/global/INDEX.md` or relevant global documentation.
- When creating, renaming, or removing project-local rules, update their index immediately.

**Rules index:**

Discover applicable rules by listing `.ai/rules/` and optional `.ai/global/rules/`; read each applicable rule before acting in its domain.

## 10. Workflows

`workflows/<YYYYMMDD>_<HHMM>_<slug>.md`

Workflows document established, repeatable procedures: development setup, deployment, migrations, authentication, verification, releases, etc.

- Explore `workflows/` before reconstructing an existing operational procedure.
- Follow documented procedures while validating their applicability to the current environment.
- Update workflows when verified procedures change.
- Skills may reference or orchestrate multiple workflows.
- Discover workflows through directory listings; no mandatory index in `AGENTS.md`.

## 11. Skills

`skills/<YYYYMMDD>_<HHMM>_<slug>.md`

Skills describe specialized agent capabilities, approaches, and reusable problem-solving methods. They may reference workflows, templates, rules, and other resources.

- Consult available skills when they could improve the work.
- Unlike rules, skills are optional unless explicitly required by an applicable instruction.
- Maintain a discoverable index in `.ai/` documentation whenever project-local skills are created, renamed, or removed; global skills remain indexed by `.ai/global/INDEX.md` or relevant global documentation.

**Skills index:**

Discover installed skills by listing `.ai/skills/` and optional `.ai/global/skills/`.

## 12. Templates

`templates/`

Reusable structures for tasks, logs, decisions, analyses, forms, rules, workflows, skills, and other artifacts.

- Discover templates through directory listings.
- Use the appropriate template when creating an artifact.
- Adapt templates to actual requirements; avoid unnecessary or empty sections.
- Improve templates when recurring shortcomings become evident.

## 13. Operating Principles

- **Work first:** every substantive activity must be tracked in `.ai/work/`.
- **Isolate execution:** use dedicated Git worktrees and branches unless explicitly instructed otherwise.
- **Preserve continuity:** keep task progress, next actions, dependencies, branch, and worktree recoverable after any context reset.
- **Investigate thoroughly:** explore repository knowledge, references, decisions, and dependencies before consequential changes.
- **Maintain provenance:** link artifacts to originating work, analyses, decisions, and conversations. Preserve relationships across moves.
- **Keep memory current:** `wiki/` for lasting understanding, `decisions/` for commitments, `logs/` for the ongoing project narrative.
- **Support asynchronous decisions:** provide comprehensive, independently answerable forms; respect partial responses.
- **Write efficiently:** favor accurate, structured, useful records over redundant narration. Do not confuse concise writing with superficial analysis.
- **Respect instructions:** applicable rules are mandatory; workflows prescribe repeatable execution, and skills provide optional specialized support.
- **Preserve `AGENTS.md`:** do not modify it without explicit user instruction. If an `.ai/workflows/` workflow applies to maintaining instructions, follow that workflow.
- **Never invent context:** verify existing state, investigate uncertainty, and preserve evidence.
