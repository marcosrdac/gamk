# Decision: use an explicit read-only status check for source divergence

- **Status:** Confirmed during implementation on 2026-11-02.
- **Originating work:** `010_20261102_2005_source-divergence-status`.
- **Investigation:** `20261102_2248_source-divergence-status`.
- **Branch/worktree:** `feat/git-ai-global-mother` / `.git-worktrees/git-ai-global-mother`.

## Decision

Expose `status [TARGET]` through the Python CLI, Bash wrapper, and PowerShell wrapper. It compares `.ai/global-manifest.json` with `global/manifest.json` and the Git checkout reachable through `.ai/global`.

The command reports three normal states:

- `current`: schema and available source identity match the recorded installation;
- `not installed`: neither the consumer manifest nor global link exists;
- `attention required`: the manifest/link is incomplete or invalid, schema differs, source commits differ, the source checkout cannot be identified, or source URLs differ/cannot be compared.

It returns zero for `current`, `not installed`, and the mother repository; it returns one for `attention required`. The consumer manifest records `installation_mode` as `full` or `local`; a local-mode consumer without `.ai/global` is normal and skips source checkout comparison. Status never writes, repairs links, updates the manifest, or compares consumer template contents.

## Rationale

A deliberate command keeps routine agent work quiet while making divergence visible when a user or agent asks for an explicit check. Commit ancestry distinguishes a source that advanced from a different history when the source checkout is available. Refusing to infer identity for copied or disconnected global directories avoids presenting a false “current” result.

## Alternatives considered

- Run the warning during every install or routine agent startup: rejected as too noisy and likely to prompt during unrelated work.
- Automatically upgrade or rewrite the consumer manifest: rejected because structural changes and customizations require user-approved, agent-led migration.
- Compare every template file: rejected for this first status check; content/customization review belongs to the structural-upgrade skill.

## Consequences

The user must explicitly run `status` to receive divergence warnings. A nonzero result is diagnostic, not permission to migrate. The structural-upgrade skill remains the path for reviewing source diffs, consumer changes, and user-approved updates.
