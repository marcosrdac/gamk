#!/usr/bin/env python3
"""Safely remove a completed GAMK feature worktree and, by default, its branch."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


BASE_BRANCH = "main"
WORKTREE_PARENT = ".git-worktrees"


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def git_text(cwd: Path, *args: str) -> str:
    result = git(cwd, *args)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def repository_root() -> Path:
    result = git(Path.cwd(), "rev-parse", "--show-toplevel")
    if result.returncode:
        raise RuntimeError("Run this command from inside the GAMK Git repository")
    return Path(result.stdout.strip()).resolve()


def registered_worktrees(root: Path) -> set[Path]:
    result = git(root, "worktree", "list", "--porcelain")
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Could not list Git worktrees")
    paths: set[Path] = set()
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            paths.add(Path(line.removeprefix("worktree ")).resolve())
    return paths


def active_task_files(target: Path) -> list[Path]:
    doing = target / ".ai/work/doing"
    if not doing.is_dir():
        return []
    return sorted(
        path for path in doing.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    )


def target_path(root: Path, requested: Path) -> Path:
    candidate = requested.expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def validate(root: Path, target: Path) -> tuple[str, list[str]]:
    issues: list[str] = []
    current_branch = git_text(root, "branch", "--show-current")
    if current_branch != BASE_BRANCH:
        issues.append(f"current checkout must be on {BASE_BRANCH!r}, not {current_branch or 'detached HEAD'!r}")

    parent = (root / WORKTREE_PARENT).resolve()
    try:
        target.relative_to(parent)
    except ValueError:
        issues.append(f"target must be inside {parent}")
    if target == root:
        issues.append("refusing to remove the main worktree")
    if not target.is_dir():
        issues.append(f"target worktree does not exist: {target}")
    elif target not in registered_worktrees(root):
        issues.append(f"target is not a registered Git worktree: {target}")

    branch = ""
    if target.is_dir():
        branch = git_text(target, "branch", "--show-current")
        if not branch:
            issues.append("target worktree is detached; cleanup requires a named feature branch")
        elif branch == BASE_BRANCH:
            issues.append(f"refusing to remove the {BASE_BRANCH} branch")

        dirty = git(target, "status", "--porcelain=v1", "--untracked-files=all")
        if dirty.returncode:
            issues.append(dirty.stderr.strip() or "could not inspect target worktree status")
        elif dirty.stdout.strip():
            issues.append("target worktree has uncommitted or untracked files")

        tasks = active_task_files(target)
        if tasks:
            issues.append(
                "target still has active tasks: "
                + ", ".join(str(path.relative_to(target)) for path in tasks)
            )

        if branch and current_branch == BASE_BRANCH:
            merged = git(root, "merge-base", "--is-ancestor", branch, BASE_BRANCH)
            if merged.returncode != 0:
                issues.append(f"branch {branch!r} is not fully integrated into {BASE_BRANCH}")

    return branch, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Remove a clean, merged feature worktree without using force."
    )
    parser.add_argument("target", type=Path, help="worktree path under .git-worktrees/")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the removal; without this flag, only validate and print the plan",
    )
    parser.add_argument(
        "--keep-branch",
        action="store_true",
        help="remove the worktree but keep its already-merged branch",
    )
    args = parser.parse_args(argv)

    try:
        root = repository_root()
        target = target_path(root, args.target)
        branch, issues = validate(root, target)
        if issues:
            print("Worktree cleanup refused:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            print("No files or Git references were changed.", file=sys.stderr)
            return 2

        print(f"Main checkout: {root}")
        print(f"Target worktree: {target}")
        print(f"Merged branch: {branch}")
        if args.keep_branch:
            print("Plan: remove the worktree and keep the merged branch.")
        else:
            print("Plan: remove the worktree and delete the merged branch safely.")
        if not args.apply:
            print("Dry run only. Re-run with --apply to perform this cleanup.")
            return 0

        removed = git(root, "worktree", "remove", str(target))
        if removed.returncode:
            raise RuntimeError(removed.stderr.strip() or "Git refused to remove the worktree")
        if not args.keep_branch:
            deleted = git(root, "branch", "-d", branch)
            if deleted.returncode:
                raise RuntimeError(deleted.stderr.strip() or "Git refused to delete the merged branch")
        pruned = git(root, "worktree", "prune")
        if pruned.returncode:
            raise RuntimeError(pruned.stderr.strip() or "Git worktree prune failed")
        print("Worktree cleanup complete.")
        return 0
    except (OSError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
