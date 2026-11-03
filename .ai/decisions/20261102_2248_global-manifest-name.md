# Decision: name the consumer provenance file `global-manifest.json`

- **Status:** Confirmed by user in conversation on 2026-11-02.
- **Originating work:** `010_20261102_2005_source-divergence-status`.
- **Branch/worktree:** `feat/git-ai-global-mother` / `.git-worktrees/git-ai-global-mother`.

## Decision

Store consumer installation identity at `.ai/global-manifest.json`. Keep the source repository's own manifest at `global/manifest.json`.

## Rationale

The name is explicit about the relationship to the reusable global source while avoiding the product-specific `git-ai-global.json` name. It distinguishes the consumer record from the source manifest by both location and filename.

## Consequences

The installer, tests, documentation, and divergence design use `.ai/global-manifest.json`. No automatic compatibility migration for the previous development-only filename is added at this point; any future compatibility behavior must be designed explicitly before release.
