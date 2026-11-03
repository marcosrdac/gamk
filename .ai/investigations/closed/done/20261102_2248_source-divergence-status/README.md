---
status: done
work: ../../../../work/closed/done/20261102_2005_source-divergence-status.md
origin: user conversation
---

# Source and installed-structure divergence

## Objective

Design a low-noise way to tell whether a consumer's installed global structure is behind, incompatible with, or disconnected from the source currently available through `.ai/global`, while preserving intentional consumer customization.

## Initial evidence

The selected consumer file is `.ai/global-manifest.json`. The installer writes:

- `format`: identifies a consumer provenance record;
- `schema_version`: identifies the expected structure contract;
- `source_url`: records the credential-free source URL when available;
- `base_commit`: records the full Git commit used for installation.

The current source also has `global/manifest.json` with its source format, repository name, and schema version. The consumer `.ai/global` link contains the local checkout path but that path must remain outside the versioned provenance record.

## Filename options under consideration

| Candidate | Strength | Concern |
| --- | --- | --- |
| `.ai/provenance.json` | Describes origin and installed identity without coupling to this product name. | “Provenance” may be unfamiliar to some users. |
| `.ai/global-source.json` | Very explicit about the relationship to `global/`. | Less future-proof if other source types are tracked later. |
| `.ai/source-manifest.json` | Combines source identity and manifest semantics. | Long and slightly technical. |
| `.ai/installation.json` | Clear that it describes the installed package. | Could be confused with installation state or logs. |
| `.ai/source.json` | Short and readable. | Too generic inside a larger `.ai/` ecosystem. |
| `.ai/manifest.json` | Familiar convention. | Does not explain what is being manifested. |

User-selected filename: `.ai/global-manifest.json`. The source-side file remains `global/manifest.json`; the two files serve different roles and locations.

## Implemented status design

The explicit `scripts/install.py status TARGET` command, exposed by both shell wrappers, compares only provenance and source identity. It reports:

1. `current`: recorded schema, source commit, and source URL agree with the available checkout; local mode is also current when its intentionally absent link is recorded;
2. `not installed`: neither the consumer manifest nor the global link exists;
3. `attention required`: the manifest/link is incomplete or invalid, the schema differs, the source commit advanced or diverged, the source checkout cannot be identified, or the source URL differs/is unavailable.

The command returns zero for `current`, `not installed`, and the mother repository; it returns one for `attention required` and does not modify any file. A consumer manifest records whether it was installed in `full` or intentional `local` mode. A local-mode consumer with no global link is normal, and source checkout comparison is skipped because there is no source path to inspect. The command does not inspect consumer template contents, Git working-tree changes, or intentional customizations. Those cases remain the responsibility of the structural-upgrade skill and the responsible agent. A status warning is therefore deliberate and low-noise rather than a prompt on every routine task.

When the available source is a Git checkout, commit ancestry distinguishes a source that advanced from a different history. When `.ai/global` points to a copied directory or otherwise cannot be tied to a checkout containing `global/manifest.json`, status reports that source identity is unavailable instead of guessing.

## Verification

Regression coverage now includes current, local mode, not installed, advanced source, schema mismatch, missing link, disconnected source, Bash forwarding, and PowerShell forwarding. The NixOS PowerShell probe remains explicitly limited to PowerShell Core and Linux filesystem behavior; it does not claim native Windows validation.

## Conclusion

The divergence design is complete. Source and consumer identity are compared only when an explicit status check is requested. No automatic upgrade, overwrite, or manifest rewrite was introduced.
