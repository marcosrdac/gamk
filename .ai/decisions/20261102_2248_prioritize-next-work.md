# Decision: defer native Windows validation and prioritize the next queue

- **Status:** Confirmed by user in conversation on 2026-11-02.
- **Originating work:** `010_20261102_2248_reprioritize-native-windows`.
- **Branch/worktree:** `feat/git-ai-global-mother` / `.git-worktrees/git-ai-global-mother`.

## Decision

Move native Windows validation from `work/next/` to `work/pool/backlog/`. Keep the Git submodule study (`010`) and source-divergence status design (`020`) in `work/next/` for consideration as the next priorities.

## Rationale

The NixOS PowerShell probe is sufficient for the current wrapper work, while native Windows execution requires a separate host or CI runner and is not currently the best use of project attention.

## Consequences

The repository continues to document that native Windows behavior is unverified, but it no longer presents that work as immediate queue priority. The next queue remains focused on distribution strategy and detecting source-versus-consumer drift.
