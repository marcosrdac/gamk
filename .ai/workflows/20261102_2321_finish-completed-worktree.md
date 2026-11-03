# Finish a completed GAMK worktree

This workflow prevents completed feature worktrees and branches from accumulating. It must be run from the main checkout, never from the worktree being removed.

## Preconditions

The target worktree is removable only when all of these are true:

- the current checkout is on `main`;
- the target is registered under `.git-worktrees/`;
- the target branch has been fast-forwarded or merged into `main`;
- the target Git status is clean, including untracked files;
- `.ai/work/doing/` contains no active task files;
- the target is not the main worktree and is not detached.

The cleanup script never uses `git worktree remove --force` and never uses `git branch -D`.

## Procedure

From the repository root:

```bash
# Inspect the checks and planned removal without changing anything.
nix shell nixpkgs#python3 --command python3 scripts/finish-worktree.py \
  .git-worktrees/<worktree-name>

# Remove the clean worktree and delete its already-merged branch.
nix shell nixpkgs#python3 --command python3 scripts/finish-worktree.py \
  .git-worktrees/<worktree-name> --apply
```

Use `--keep-branch` only when the merged branch is intentionally needed for a release, audit, or later reference. The default removes both the worktree and its merged branch. Git's normal `worktree remove` and `branch -d` checks remain the final safety barrier.

Afterwards, verify:

```bash
git worktree list
git branch --merged main
git worktree prune
```

`git worktree prune` only removes stale administrative records; it does not force-delete a live or dirty worktree.

## If cleanup is refused

Do not add a force flag. Read the reported condition and resolve it explicitly:

- active task: finish or pause the task, preserving its `.ai/work/` state;
- dirty files: inspect, commit, move, or intentionally preserve them;
- unmerged branch: integrate it into `main` or abandon it with a recorded reason;
- detached branch: recover the commit and name/record the branch before cleanup.

The worktree lifecycle is therefore:

```text
create → implement → test → close task → integrate into main → dry-run cleanup → apply cleanup
```
