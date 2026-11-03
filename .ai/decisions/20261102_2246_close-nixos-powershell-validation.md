# Decision: close NixOS PowerShell pre-validation and defer native Windows

- **Status:** Confirmed by user in conversation on 2026-11-02.
- **Originating work:** `010_20261102_2200_validate-windows-installers`.
- **Branch/worktree:** `feat/git-ai-global-mother` / `.git-worktrees/git-ai-global-mother`.

## Decision

Treat the NixOS `pwsh` probe as the completed scope for the current validation task. It covers PowerShell parsing, wrapper argument forwarding, safe planning, installation and blocking behavior, but it must not be described as native Windows validation.

Move native Windows testing to the backlog task `.ai/work/pool/backlog/20261102_2246_validate-native-windows-installers.md`.

## Rationale

The user accepted the reproducible NixOS probe as sufficient for the current integration. Keeping native Windows work separate preserves an accurate platform claim while allowing the tested implementation to move forward.

## Consequences

The installer is integrated with documented Linux/NixOS PowerShell evidence. Native NTFS symlink/junction behavior, Windows permissions, and Windows path semantics remain explicitly unverified until the planned task runs.
