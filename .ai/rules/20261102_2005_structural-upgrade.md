# Mandatory structural-upgrade rule

When planning or performing a structural upgrade in a consumer project, read and follow `.ai/skills/20261102_2005_structural-upgrade.md`.

Do not treat template diffs as authority to overwrite project state. Explain benefits, costs, risks, and legacy reconstruction effort for each change, get the user's approval for each change, preserve unapproved/legacy material, and update provenance only after approved work is complete.

The installer does not edit consumer `.gitignore`, `.git/info/exclude`, or the Git index. Explain that the user should ignore the local absolute `.ai/global` symlink before committing any consumer changes.
