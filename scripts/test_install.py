"""Regression tests for safe plan/install/repair behavior."""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import install


REPOSITORY = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)

    def project(self, name="consumer", git=True):
        root = self.workspace / name
        root.mkdir()
        if git:
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
        return root

    def snapshot(self, root):
        return sorted(
            (path.relative_to(root).as_posix(), path.is_symlink(), path.readlink().as_posix() if path.is_symlink() else None)
            for path in root.rglob("*")
        )

    def invoke(self, command, target, *extra):
        output = subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts" / "install.py"), command, str(target), *extra],
            capture_output=True,
            text=True,
            check=False,
        )
        return output

    def invoke_cli(self, command, target=None, *extra):
        args = [sys.executable, str(REPOSITORY / "scripts" / "install.py"), command]
        if target is not None:
            args.append(str(target))
        args.extend(extra)
        return subprocess.run(args, capture_output=True, text=True, check=False)

    def test_plan_is_read_only_and_contains_paths_commit_and_migration_instructions(self):
        root = self.project()
        (root / "AGENTS.md").write_text("existing instructions\n")
        before = self.snapshot(root)

        result = self.invoke("plan", root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(root), before)
        self.assertIn(str(root / "AGENTS.md"), result.stdout)
        self.assertIn(install.source_identity(REPOSITORY)[0], result.stdout)
        self.assertIn("do not replace it wholesale", result.stdout)
        self.assertIn(str(REPOSITORY / "global" / "templates" / "project" / "AGENTS.md"), result.stdout)

    def test_root_and_consumer_agents_are_aligned(self):
        root = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
        template = (REPOSITORY / "global" / "templates" / "project" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(template.count("**Project instructions:**"), 1)
        self.assertEqual(root.count("**Project instructions:**"), 1)
        for shared_contract in (
            "**Optional shared context:**",
            "explicit task instructions take precedence over project instructions",
            "**Discovery:** Treat `.ai/` as the repository's persistent memory.",
            "Every investigation, form creation, documentation change, or other substantive activity must be tracked by a work task.",
            "**Project instructions:** At startup, discover applicable project rules in `.ai/rules/`",
            "## 3. Work Management",
            "## 4. Logs",
            "## 5. Decisions",
            "## 6. Wiki",
            "## 7. Investigations",
            "## 8. Forms",
            "## 9. Workflows",
            "## 10. Skills",
            "## 11. Rules",
            "## 12. Templates",
            "## 13. Operating Principles",
        ):
            with self.subTest(shared_contract=shared_contract):
                self.assertIn(shared_contract, root)
                self.assertIn(shared_contract, template)

    def test_mother_extension_names_local_rules_and_workflow(self):
        text = (REPOSITORY / ".ai/templates/mother-AGENTS.extensions.md").read_text(encoding="utf-8")
        self.assertIn("Read every applicable mother-local rule in `.ai/rules/`", text)
        self.assertIn("mother-local workflow `update-agent-instructions.md`", text)
        self.assertIn("never installed into consumer projects", text)

    def test_consumer_agents_describe_global_directory_and_symlink_loading(self):
        text = (REPOSITORY / "global" / "templates" / "project" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("as a directory or symlink", text)
        self.assertIn("Follow any “Always Read” instructions there", text)
        self.assertIn("applicable mandatory rules", text)
        self.assertIn("must not be required for collaborators", text)
        for mandatory_rule in ("rules/system-maintenance.md", "rules/context-loading.md"):
            with self.subTest(mandatory_rule=mandatory_rule):
                self.assertIn(mandatory_rule, (REPOSITORY / "global" / "INDEX.md").read_text(encoding="utf-8"))
        self.assertIn("follow every “Always Read” entry", (REPOSITORY / "global" / "rules" / "context-loading.md").read_text(encoding="utf-8"))

    def test_consumer_agents_do_not_embed_mother_only_skill_or_rule_names(self):
        text = (REPOSITORY / "global" / "templates" / "project" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertNotIn("20261102_2005_agents-parity.md", text)
        self.assertNotIn("20261102_2005_structural-upgrade.md", text)
        self.assertIn("optional `.ai/global/rules/`", text)
        self.assertIn("optional `.ai/global/skills/`", text)
        self.assertNotIn("canonical source repository may maintain a local index", text)

    def test_mother_agents_generator_is_deterministic_and_separates_extensions(self):
        result = self.invoke_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        generated = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
        template = (REPOSITORY / "global" / "templates" / "project" / "AGENTS.md").read_text(encoding="utf-8")
        extension = (REPOSITORY / ".ai" / "templates" / "mother-AGENTS.extensions.md").read_text(encoding="utf-8").strip()

        self.assertTrue(generated.startswith(template.rstrip() + "\n\n"))
        self.assertEqual(generated.count("# Agent Instructions"), 1)
        self.assertTrue(generated.endswith(extension + "\n"))
        self.assertIn("mother-local rule", generated)
        self.assertNotIn("Mother repository extensions", template)
        self.assertNotIn(".ai/rules/20261102_2005_agents-parity.md", template)

        check = subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts" / "generate_mother_agents.py"), "--check"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(check.returncode, 0, check.stderr)

        # A stale generated file must be detected without modifying it.
        (REPOSITORY / "AGENTS.md").write_text("stale\n", encoding="utf-8")
        stale = self.invoke_generator("--check")
        self.assertEqual(stale.returncode, 1)
        self.assertEqual((REPOSITORY / "AGENTS.md").read_text(encoding="utf-8"), "stale\n")
        repaired = self.invoke_generator()
        self.assertEqual(repaired.returncode, 0, repaired.stderr)

    def invoke_generator(self, *args):
        return subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts" / "generate_mother_agents.py"), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_install_fails_before_any_write_for_existing_agents_or_ai_directory(self):
        for signal in ("agents", "ai"):
            with self.subTest(signal=signal):
                root = self.project(signal)
                if signal == "agents":
                    (root / "AGENTS.md").write_text("owner instructions\n")
                else:
                    (root / ".ai").mkdir()
                    (root / ".ai" / "keep.md").write_text("keep\n")
                before = self.snapshot(root)

                result = self.invoke("install", root)

                self.assertEqual(result.returncode, 2)
                self.assertIn("No files were changed", result.stderr)
                self.assertIn("plan", result.stderr)
                self.assertEqual(self.snapshot(root), before)

    def test_known_agent_configuration_blocks_install(self):
        root = self.project()
        (root / ".cursor" / "rules").mkdir(parents=True)
        (root / ".cursor" / "rules" / "project.mdc").write_text("rule\n")
        before = self.snapshot(root)

        result = self.invoke_cli("install", root, "--mode", "full")

        self.assertEqual(result.returncode, 2)
        self.assertIn(".cursor/rules", result.stderr)
        self.assertEqual(self.snapshot(root), before)

    def test_non_ai_destination_collision_is_found_before_writes(self):
        root = self.project()
        (root / "README.md").write_text("existing project readme\n")
        before = self.snapshot(root)
        result = install.preflight(install.Target(root, root / ".ai"), "full")
        self.assertFalse(result.signals)
        self.assertEqual(self.snapshot(root), before)

    def test_clean_install_creates_structure_manifest_and_local_symlink_without_git_mutations(self):
        root = self.project()
        result = self.invoke("install", root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((root / "AGENTS.md").is_file())
        self.assertTrue((root / ".ai" / "work" / "doing").is_dir())
        self.assertEqual((root / ".ai" / "global").resolve(), REPOSITORY / "global")
        manifest = json.loads((root / ".ai" / "git-ai-global.json").read_text())
        self.assertEqual(manifest["format"], "git-ai-global-consumer")
        self.assertEqual(manifest["base_commit"], install.source_identity(REPOSITORY)[0])
        self.assertEqual(manifest["schema_version"], install.SCHEMA_VERSION)
        self.assertNotIn(str(REPOSITORY), json.dumps(manifest))
        self.assertIsNone(manifest["source_url"])
        self.assertFalse((root / ".gitignore").exists())
        self.assertEqual(
            subprocess.run(["git", "-C", str(root), "status", "--short"], capture_output=True, text=True).stdout.count(".gitignore"),
            0,
        )
        self.assertIn("ignore `.ai/global`", result.stdout)

    def test_local_mode_does_not_create_global_link(self):
        root = self.project()
        result = self.invoke_cli("install", root, "--mode", "local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((root / ".ai" / "global").exists())
        self.assertTrue((root / ".ai" / "git-ai-global.json").exists())

    def test_manifest_records_source_url_when_source_has_origin(self):
        root = self.project()
        with patch.object(install, "source_identity", return_value=("abc123", "https://example.invalid/git-ai-global.git")):
            result = install.preflight(install.Target(root, root / ".ai"))
            self.assertEqual(result.source_url, "https://example.invalid/git-ai-global.git")

    def test_source_url_credentials_are_not_persisted(self):
        with patch.object(install, "run_git") as git:
            git.side_effect = [
                subprocess.CompletedProcess([], 0, "abc123\n", ""),
                subprocess.CompletedProcess([], 0, "https://token:secret@example.invalid/repo.git\n", ""),
            ]
            self.assertEqual(
                install.source_identity(REPOSITORY)[1],
                "https://example.invalid/repo.git",
            )

    def test_exact_global_destination_only_installs_link(self):
        root = self.project()
        link = root / ".ai" / "global"
        result = self.invoke_cli("install", link, "--mode", "global")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(link.resolve(), REPOSITORY / "global")
        self.assertFalse((root / "AGENTS.md").exists())
        self.assertFalse((root / ".ai" / "git-ai-global.json").exists())

    def test_global_link_install_is_idempotent_when_link_already_matches(self):
        root = self.project()
        link = root / ".ai" / "global"
        link.parent.mkdir()
        link.symlink_to(REPOSITORY / "global", target_is_directory=True)
        result = self.invoke_cli("install", link, "--mode", "global")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(link.resolve(), REPOSITORY / "global")

    def test_global_mode_refuses_occupied_destination_without_mutation(self):
        root = self.project()
        link = root / ".ai" / "global"
        link.mkdir(parents=True)
        (link / "owned.txt").write_text("keep\n")
        before = self.snapshot(root)
        result = self.invoke_cli("install", link, "--mode", "global")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(root), before)

    def test_mother_commands_are_read_only_and_refuse_missing_link(self):
        link = REPOSITORY / ".ai" / "global"
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), "../global")
        for command in ("plan-mother", "init-mother"):
            result = self.invoke_cli(command)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(link.is_symlink())
            self.assertEqual(os.readlink(link), "../global")

        copied_source = self.workspace / "source-copy"
        shutil.copytree(REPOSITORY, copied_source, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        missing_link = copied_source / ".ai" / "global"
        missing_link.unlink()
        for command in ("plan-mother", "init-mother"):
            result = subprocess.run(
                [sys.executable, str(copied_source / "scripts" / "install.py"), command],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(missing_link.exists())
            self.assertFalse(missing_link.is_symlink())

    def test_repair_link_repairs_broken_symlink_and_refuses_real_directory(self):
        root = self.project()
        link = root / ".ai" / "global"
        link.parent.mkdir()
        link.symlink_to(root / "missing", target_is_directory=True)

        result = self.invoke_cli("repair-link", root / ".ai" / "global")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(link.resolve(), REPOSITORY / "global")

        link.unlink()
        link.mkdir()
        before = self.snapshot(root)
        refused = self.invoke_cli("repair-link", root / ".ai" / "global")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("Refusing to replace", refused.stderr)
        self.assertEqual(self.snapshot(root), before)

    def test_install_rolls_back_new_files_if_link_creation_fails(self):
        root = self.project()
        before = self.snapshot(root)
        target = install.resolve_target(root, root)
        result = install.preflight(target, "full")
        with patch.object(install, "create_link", side_effect=OSError("simulated link failure")):
            with self.assertRaisesRegex(OSError, "simulated link failure"):
                install.install(target, result, "full")
        self.assertEqual(self.snapshot(root), before)

    def test_preflight_detects_manifest_directory_collision(self):
        root = self.project()
        (root / ".ai" / "git-ai-global.json").mkdir(parents=True)
        result = install.preflight(install.Target(root, root / ".ai"))
        self.assertTrue(any(signal.path == root / ".ai" / "git-ai-global.json" for signal in result.signals))

    def test_repair_link_preflight_does_not_block_on_existing_project_context(self):
        root = self.project()
        (root / "AGENTS.md").write_text("existing\n")
        (root / ".ai").mkdir()
        target = install.resolve_target(root, root)
        result = install.preflight(target, "repair")
        self.assertFalse(result.signals)
        link = root / ".ai" / "global"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.repair_link(target, result), 0)
        self.assertTrue(link.is_symlink())

    def test_repair_link_blocks_existing_non_symlink_without_creating_ai_dir(self):
        root = self.project()
        target = install.resolve_target(root, root)
        (root / ".ai").write_text("not a directory")
        before = self.snapshot(root)
        result = self.invoke_cli("repair-link", root)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(root), before)

    def test_installing_into_mother_refuses_without_mutation(self):
        target = install.Target(REPOSITORY, REPOSITORY / ".ai", "project")
        result = install.preflight(target)
        self.assertTrue(any("mother repository" in signal.reason for signal in result.signals))

    def test_installing_into_mother_never_creates_absolute_consumer_link(self):
        target = install.Target(REPOSITORY, REPOSITORY / ".ai", "project")
        result = install.preflight(target)
        before = sorted(path.relative_to(REPOSITORY).as_posix() for path in REPOSITORY.rglob("*") if ".git" not in path.parts)
        self.assertEqual(install.install(target, result, "full"), 2)
        after = sorted(path.relative_to(REPOSITORY).as_posix() for path in REPOSITORY.rglob("*") if ".git" not in path.parts)
        self.assertEqual(after, before)

    def test_install_fails_before_writing_when_global_link_destination_is_occupied(self):
        root = self.project()
        (root / ".ai").mkdir()
        (root / ".ai" / "global").mkdir()
        before = self.snapshot(root)
        result = self.invoke_cli("install", root, "--mode", "full")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(root), before)

    def test_preflight_detects_top_level_known_agent_files(self):
        root = self.project()
        (root / "CLAUDE.md").write_text("instructions\n")
        signals = install.collect_signals(install.Target(root, root / ".ai", "project"), REPOSITORY)
        self.assertTrue(any(signal.path == root / "CLAUDE.md" for signal in signals))

    def test_preflight_detects_nested_agents_file(self):
        root = self.project()
        nested = root / "packages" / "api" / "AGENTS.md"
        nested.parent.mkdir(parents=True)
        nested.write_text("nested instructions\n")
        signals = install.collect_signals(install.Target(root, root / ".ai", "project"), REPOSITORY)
        self.assertTrue(any(signal.path == nested for signal in signals))

    def test_target_resolution_accepts_ai_dir_and_global_destination(self):
        root = self.project()
        self.assertEqual(install.resolve_target(root / ".ai", root).ai_dir, root / ".ai")
        resolved = install.resolve_target(root / ".ai" / "global", root)
        self.assertEqual(resolved.root, root)
        self.assertEqual(resolved.kind, "global")

    def test_global_only_mode_does_not_require_project_template_signal_clearance(self):
        root = self.project()
        (root / "AGENTS.md").write_text("existing project instructions\n")
        result = self.invoke_cli("install", root, "--mode", "global")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((root / "AGENTS.md").read_text(), "existing project instructions\n")
        self.assertEqual((root / ".ai" / "global").resolve(), REPOSITORY / "global")

    def test_local_mode_blocks_existing_agents_and_manifest_destinations(self):
        for relative in ("AGENTS.md", ".ai/git-ai-global.json"):
            with self.subTest(relative=relative):
                root = self.project(relative.replace("/", "_"))
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("owner data\n")
                before = self.snapshot(root)
                result = self.invoke_cli("install", root, "--mode", "local")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.snapshot(root), before)

    def test_no_subcommand_invokes_read_only_plan_through_shell_wrapper(self):
        root = self.project()
        result = subprocess.run(
            ["bash", str(REPOSITORY / "scripts" / "install.sh"), str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No known migration signals", result.stdout)

    def test_python_free_copy_installer_copies_minimal_files_and_refuses_existing_context(self):
        root = self.project()
        copied = subprocess.run(
            ["bash", str(REPOSITORY / "scripts" / "copy-install.sh"), str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(copied.returncode, 0, copied.stderr)
        self.assertTrue((root / "AGENTS.md").is_file())
        self.assertTrue((root / ".ai" / "work" / "doing").is_dir())
        self.assertFalse((root / ".ai" / "git-ai-global.json").exists())

        other = self.project("copy-conflict")
        (other / "AGENTS.md").write_text("keep\n")
        before = self.snapshot(other)
        refused = subprocess.run(
            ["bash", str(REPOSITORY / "scripts" / "copy-install.sh"), str(other)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(refused.returncode, 2)
        self.assertIn("No files were copied", refused.stderr)
        self.assertEqual(self.snapshot(other), before)

    def test_subprocess_never_auto_merges_existing_agents_even_with_yes(self):
        root = self.project()
        original = "user-owned\n"
        (root / "AGENTS.md").write_text(original)
        result = self.invoke("install", root, "--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((root / "AGENTS.md").read_text(), original)


if __name__ == "__main__":
    unittest.main()
