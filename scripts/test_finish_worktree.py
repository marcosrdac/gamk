"""Regression tests for safe cleanup of completed feature worktrees."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "scripts" / "finish-worktree.py"


class FinishWorktreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.git("init", "--quiet", "-b", "main", str(self.root))
        self.git("-C", str(self.root), "config", "user.name", "GAMK test")
        self.git("-C", str(self.root), "config", "user.email", "gamk-test@example.invalid")
        doing = self.root / ".ai/work/doing"
        doing.mkdir(parents=True)
        (doing / ".gitkeep").write_text("", encoding="utf-8")
        (self.root / "README.md").write_text("test\n", encoding="utf-8")
        self.git("-C", str(self.root), "add", ".")
        self.git("-C", str(self.root), "commit", "--quiet", "-m", "initial")
        self.target = self.root / ".git-worktrees" / "feature"
        self.git("-C", str(self.root), "worktree", "add", "--quiet", "-b", "feature", str(self.target), "main")
        self.addCleanup(self.remove_fixture_worktree)

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
        if check and result.returncode:
            raise AssertionError(f"git failed: {' '.join(args)}\n{result.stderr}")
        return result

    def run_cleanup(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def remove_fixture_worktree(self):
        if self.target.exists():
            self.git("-C", str(self.root), "worktree", "remove", "--force", str(self.target), check=False)
        self.git("-C", str(self.root), "branch", "-D", "feature", check=False)
        self.git("-C", str(self.root), "worktree", "prune", check=False)

    def test_dry_run_keeps_clean_merged_worktree(self):
        result = self.run_cleanup(str(self.target))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run only", result.stdout)
        self.assertTrue(self.target.is_dir())
        self.assertIn("feature", self.git("-C", str(self.root), "branch", "--list").stdout)

    def test_dirty_worktree_is_refused_without_changes(self):
        (self.target / "README.md").write_text("changed\n", encoding="utf-8")

        result = self.run_cleanup(str(self.target), "--apply")

        self.assertEqual(result.returncode, 2)
        self.assertIn("uncommitted or untracked", result.stderr)
        self.assertIn("No files or Git references were changed", result.stderr)
        self.assertTrue(self.target.is_dir())

    def test_active_task_is_refused_even_when_ignored(self):
        active = self.target / ".ai/work/doing/010_active.md"
        active.write_text("active\n", encoding="utf-8")
        exclude_path = Path(
            self.git("-C", str(self.target), "rev-parse", "--git-path", "info/exclude").stdout.strip()
        )
        exclude = exclude_path if exclude_path.is_absolute() else self.target / exclude_path
        exclude.write_text(".ai/work/doing/010_active.md\n", encoding="utf-8")

        result = self.run_cleanup(str(self.target), "--apply")

        self.assertEqual(result.returncode, 2)
        self.assertIn("target still has active tasks", result.stderr)
        self.assertTrue(self.target.is_dir())

    def test_apply_removes_clean_worktree_and_merged_branch(self):
        result = self.run_cleanup(str(self.target), "--apply")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Worktree cleanup complete", result.stdout)
        self.assertFalse(self.target.exists())
        self.assertNotIn("feature", self.git("-C", str(self.root), "branch", "--list").stdout)
        self.assertNotIn(str(self.target), self.git("-C", str(self.root), "worktree", "list").stdout)


if __name__ == "__main__":
    unittest.main()
