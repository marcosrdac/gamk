#!/usr/bin/env python3
"""Plan, inspect, install, and repair GAMK context in consumer projects."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

SCHEMA_VERSION = 3
PROJECT_NAME = "GAMK"
PROJECT_SLUG = "gamk"
SOURCE_MANIFEST_FORMAT = "gamk-source"
CONSUMER_MANIFEST_FORMAT = "gamk-consumer"
LEGACY_SOURCE_MANIFEST_FORMAT = "git-ai-global-source"
LEGACY_CONSUMER_MANIFEST_FORMAT = "git-ai-global-consumer"
LEGACY_REPOSITORY_NAME = "git-ai-global"
MANIFEST = Path(".ai/global-manifest.json")
PROJECT_DIRECTORIES = (
    "decisions", "forms/creating", "forms/pending", "forms/answered",
    "analyses/doing", "analyses/done", "analyses/wontdo",
    "logs", "rules", "skills", "templates", "wiki", "work/doing", "work/next",
    "work/pool/backlog", "work/pool/blocked", "work/pool/ideas",
    "work/closed/done", "work/closed/wontdo", "workflows",
)
AGENT_FILES = (
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules", ".clinerules",
    ".windsurfrules", ".github/copilot-instructions.md", ".opencode/AGENTS.md",
    ".opencode/instructions.md",
)
AGENT_DIRS = (
    ".cursor/rules", ".github/instructions", ".cline/rules", ".roo/rules",
    ".windsurf/rules",
)
SKIP_NESTED = {".git", ".hg", ".svn", ".ai", "node_modules", ".venv", "venv", "vendor"}


@dataclass(frozen=True)
class Target:
    root: Path
    ai_dir: Path
    kind: str = "project"  # project, ai, or global

    @property
    def global_link(self) -> Path:
        return self.ai_dir / "global"


@dataclass(frozen=True)
class Signal:
    path: Path
    reason: str


@dataclass(frozen=True)
class Preflight:
    signals: tuple[Signal, ...]
    source_root: Path
    source_commit: str
    source_url: Optional[str]


def run_git(args: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


def git_root(path: Path) -> Optional[Path]:
    result = run_git(("-C", str(path), "rev-parse", "--show-toplevel"), path)
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else None


def source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def resolve_target(requested: Optional[Path], cwd: Path) -> Target:
    candidate = cwd.resolve() if requested is None else requested.expanduser()
    if not candidate.is_absolute():
        candidate = cwd / candidate
    candidate = Path(os.path.abspath(str(candidate)))
    if candidate.name == "global" and candidate.parent.name == ".ai":
        root = git_root(candidate.parent.parent) or candidate.parent.parent.resolve()
        return Target(root, candidate.parent, "global")
    if candidate.name == ".ai":
        root = git_root(candidate.parent) or candidate.parent.resolve()
        return Target(root, candidate, "ai")
    root = git_root(candidate) or candidate.resolve()
    return Target(root, root / ".ai")


def source_identity(source: Path) -> tuple[str, Optional[str]]:
    commit = run_git(("-C", str(source), "rev-parse", "HEAD"), source)
    if commit.returncode:
        raise RuntimeError(f"Could not determine source Git commit at {source}")
    remote = run_git(("-C", str(source), "remote", "get-url", "origin"), source)
    url = remote.stdout.strip() if remote.returncode == 0 else None
    if url and "://" in url:
        scheme, rest = url.split("://", 1)
        authority, sep, tail = rest.partition("/")
        if "@" in authority:
            authority = authority.rsplit("@", 1)[1]
        url = f"{scheme}://{authority}{sep}{tail}"
    return commit.stdout.strip(), url or None


def is_source_manifest(data: object) -> bool:
    if not isinstance(data, dict) or not isinstance(data.get("schema_version"), int):
        return False
    identity = (data.get("format"), data.get("repository_name"))
    return identity in (
        (SOURCE_MANIFEST_FORMAT, PROJECT_SLUG),
        (LEGACY_SOURCE_MANIFEST_FORMAT, LEGACY_REPOSITORY_NAME),
    )


def source_manifest(source: Path) -> dict[str, object]:
    path = source / "global/manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Invalid or missing source manifest {path}: {error}") from error
    if not is_source_manifest(data):
        raise RuntimeError(f"Unrecognized {PROJECT_NAME} source manifest: {path}")
    return data


def source_manifest_from_global(global_dir: Path) -> dict[str, object]:
    path = global_dir / "manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Invalid or missing global source manifest {path}: {error}") from error
    if not is_source_manifest(data):
        raise RuntimeError(f"Unrecognized {PROJECT_NAME} source manifest: {path}")
    return data


def consumer_manifest(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Invalid consumer manifest {path}: {error}") from error
    if (not isinstance(data, dict) or data.get("format") not in (CONSUMER_MANIFEST_FORMAT, LEGACY_CONSUMER_MANIFEST_FORMAT)
            or not isinstance(data.get("schema_version"), int)
            or not isinstance(data.get("base_commit"), str)
            or not data.get("base_commit")
            or not isinstance(data.get("source_url"), (str, type(None)))):
        raise RuntimeError(f"Unrecognized {PROJECT_NAME} consumer manifest: {path}")
    installation_mode = data.get("installation_mode", "full")
    if not isinstance(installation_mode, str) or installation_mode not in ("full", "local"):
        raise RuntimeError(f"Unrecognized consumer installation mode: {path}")
    return data


def source_checkout_for_global(global_dir: Path) -> Optional[Path]:
    try:
        resolved_global = global_dir.resolve(strict=True)
        candidate = git_root(resolved_global)
        if candidate is None:
            return None
        if (candidate / "global/manifest.json").resolve(strict=True) != (resolved_global / "manifest.json").resolve(strict=True):
            return None
        return candidate
    except OSError:
        return None


def source_commit_is_ancestor(source: Path, base_commit: str, current_commit: str) -> Optional[bool]:
    result = run_git(("-C", str(source), "merge-base", "--is-ancestor", base_commit, current_commit), source)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def template_destinations(source: Path) -> tuple[Path, ...]:
    template = source / ".ai/templates/project"
    if not template.is_dir():
        raise RuntimeError(f"Consumer template directory not found: {template}")
    result = []
    for item in template.rglob("*"):
        if not item.is_file() or item.name == ".gitkeep" or item.relative_to(template) == Path("AGENTS.md"):
            continue
        rel = item.relative_to(template)
        result.append(Path(".ai", *rel.parts[1:]) if rel.parts[0] == ".ai" else rel)
    return tuple(result)


def collect_signals(target: Target, source: Path, mode: str = "full") -> tuple[Signal, ...]:
    signals: list[Signal] = []
    root = target.root

    if target.kind == "global" or mode == "global":
        link = target.global_link
        if path_exists(link):
            try:
                valid = link.resolve(strict=True) == (source / "global").resolve(strict=True)
            except OSError:
                valid = False
            if not valid:
                signals.append(Signal(link, "global link destination is occupied"))
        return tuple(signals)

    if mode == "repair":
        return ()

    if root.resolve() == source.resolve():
        return (Signal(target.ai_dir, "mother repository context is managed separately"),)

    if mode == "full":
        for relative in AGENT_FILES:
            path = root / relative
            if path_exists(path):
                signals.append(Signal(path, "existing agent instructions/configuration"))
        if mode == "full" and path_exists(target.ai_dir):
            signals.append(Signal(target.ai_dir, "existing agent context directory"))
        for relative in AGENT_DIRS:
            path = root / relative
            if path.is_dir():
                signals.append(Signal(path, "known agent configuration directory"))
        for relative in (".ai/INDEX.md", ".ai/README.md", ".ai/memory", ".ai/local"):
            path = root / relative
            if path_exists(path):
                signals.append(Signal(path, "existing project context path"))
        for child in root.iterdir():
            if child.name.lower() == "agents.md" and child != root / "AGENTS.md":
                signals.append(Signal(child, "additional root agent instruction file"))
        for pattern, reason in (
            (".github/instructions/**/*.md", "GitHub agent instruction file"),
            (".cursor/rules/**/*.mdc", "Cursor agent rule file"),
            (".claude/commands/**/*.md", "Claude agent command file"),
            (".opencode/command/**/*.md", "OpenCode command file"),
        ):
            signals.extend(Signal(path, reason) for path in root.glob(pattern) if path_exists(path))
        for directory, dirnames, filenames in os.walk(root):
            dirnames[:] = [name for name in dirnames if name not in SKIP_NESTED]
            if "AGENTS.md" in filenames:
                path = Path(directory) / "AGENTS.md"
                if path != root / "AGENTS.md":
                    signals.append(Signal(path, "nested AGENTS.md instruction file"))

    if mode != "global":
        file_destinations = {root / p for p in template_destinations(source)}
        directory_destinations = {target.ai_dir, *(target.ai_dir / p for p in PROJECT_DIRECTORIES)}
        if mode == "local":
            for path in (root / "AGENTS.md", root / MANIFEST):
                if path.is_dir():
                    signals.append(Signal(path, "planned file destination is a directory"))
                elif path_exists(path):
                    signals.append(Signal(path, "planned file destination is occupied"))
        if mode == "full" and path_exists(root / "AGENTS.md") and not any(s.path == root / "AGENTS.md" for s in signals):
            signals.append(Signal(root / "AGENTS.md", "planned agent instruction destination is occupied"))
        for path in file_destinations:
            if path.is_dir():
                signals.append(Signal(path, "planned file destination is a directory"))
            elif path_exists(path) and not any(s.path == path for s in signals):
                signals.append(Signal(path, "planned file destination is occupied"))
        manifest_path = root / MANIFEST
        if path_exists(manifest_path) and not any(s.path == manifest_path for s in signals):
            signals.append(Signal(manifest_path, "consumer manifest destination is occupied"))
        for path in directory_destinations:
            if path_exists(path) and not path.is_dir():
                signals.append(Signal(path, "planned directory destination is not a directory"))
        if mode == "full" and path_exists(target.global_link):
            try:
                valid = target.global_link.is_symlink() and target.global_link.resolve(strict=True) == (source / "global").resolve(strict=True)
            except OSError:
                valid = False
            if not valid:
                signals.append(Signal(target.global_link, "planned global link destination is occupied"))

    if mode == "local" and path_exists(target.global_link):
        try:
            valid = target.global_link.is_symlink() and target.global_link.resolve(strict=True) == (source / "global").resolve(strict=True)
        except OSError:
            valid = False
        if not valid:
            signals.append(Signal(target.global_link, "existing global link requires review"))

    seen: set[tuple[Path, str]] = set()
    unique: list[Signal] = []
    for signal in signals:
        key = (signal.path, signal.reason)
        if key not in seen:
            seen.add(key)
            unique.append(signal)
    return tuple(unique)


def preflight(target: Target, mode: str = "full") -> Preflight:
    if not target.root.is_dir():
        raise RuntimeError(f"Target project directory does not exist: {target.root}")
    if not target.ai_dir.is_relative_to(target.root):
        raise RuntimeError("The .ai context directory must be inside the target project")
    source = source_root()
    manifest = source_manifest(source)
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise RuntimeError(f"Installer schema {SCHEMA_VERSION} does not match source schema {manifest['schema_version']}")
    commit, url = source_identity(source)
    return Preflight(collect_signals(target, source, mode), source, commit, url)


def render_migration_prompt(target: Target, result: Preflight) -> str:
    findings = "\n".join(f"- `{s.path}` — {s.reason}" for s in result.signals) or "- No known signals (not a semantic compatibility guarantee)."
    known = "\n".join(f"- `{target.root / p}`" for p in (*AGENT_FILES, *AGENT_DIRS))
    source_agents = result.source_root / "AGENTS.md"
    consumer_agents = result.source_root / ".ai/templates/project/AGENTS.md"
    return f"""Migration request for the agent responsible for this repository

Target repository: `{target.root}`
Target context directory: `{target.ai_dir}`
Source checkout: `{result.source_root}`
Source Git URL: `{result.source_url or '(no origin remote configured)'}`
Source base commit: `{result.source_commit}`
Structural schema: `{SCHEMA_VERSION}`

Detected signals:
{findings}

Inspect relevant files before changing anything:
{known}
- Mother instructions: `{source_agents}`
- Consumer template: `{consumer_agents}`
- Existing target context: `{target.ai_dir}`
- Files that will be added if installation is approved: `{target.root / 'AGENTS.md'}`, `{target.root / MANIFEST}`, and the documented `.ai/` directory structure.

Preserve project instructions, current behavior, and legacy material. Integrate an existing root AGENTS.md responsibly; do not replace it wholesale. Explain structural changes and tradeoffs, identify legacy content requiring reconstruction, and ask the user before consequential or uncertain edits. Do not delete residual files merely to match the template.

After the user-approved migration is complete, rerun install; its preflight will run again.
"""


def print_plan(target: Target, result: Preflight) -> None:
    print(f"Target: {target.root}\nContext: {target.ai_dir}\nSource commit: {result.source_commit}")
    if result.signals:
        print("\nMigration signals:")
        for signal in result.signals:
            print(f"- {signal.path}: {signal.reason}")
    else:
        print("\nNo known migration signals detected (not a semantic compatibility guarantee).")
    print("\n" + render_migration_prompt(target, result))


def print_blocked(target: Target, result: Preflight) -> None:
    print(f"Installation blocked for {target.root}:", file=sys.stderr)
    for signal in result.signals:
        print(f"- {signal.path}: {signal.reason}", file=sys.stderr)
    print("No files were changed. Run plan for the migration prompt:", file=sys.stderr)
    print(f"  {Path(__file__).resolve()} plan {target.root}", file=sys.stderr)


def status(target: Target) -> int:
    if not target.root.is_dir():
        raise RuntimeError(f"Target project directory does not exist: {target.root}")
    if target.root.resolve() == source_root().resolve():
        print("Status: mother repository")
        print("Use plan-mother or init-mother to inspect the tracked source link.")
        return 0

    manifest_path = target.root / MANIFEST
    link = target.global_link
    if not path_exists(manifest_path):
        if path_exists(link):
            print("Status: incomplete")
            print(f"Consumer manifest is missing: {manifest_path}")
            print("No files were changed.")
            return 1
        print("Status: not installed")
        print(f"Consumer manifest is absent: {manifest_path}")
        return 0

    try:
        consumer = consumer_manifest(manifest_path)
    except RuntimeError as error:
        print("Status: invalid")
        print(f"- {error}")
        print("No files were changed.")
        return 1

    base_commit = str(consumer["base_commit"])
    consumer_schema = int(consumer["schema_version"])
    installation_mode = str(consumer.get("installation_mode", "full"))
    findings: list[str] = []
    source_checked = False
    source_checkout: Optional[Path] = None
    current_commit: Optional[str] = None
    current_url: Optional[str] = None
    source_schema: Optional[int] = None

    print(f"Consumer: {target.root}")
    print(f"Manifest: {manifest_path}")
    print(f"Installation mode: {installation_mode}")
    print(f"Recorded source commit: {base_commit}")
    print(f"Recorded schema: {consumer_schema}")

    if not path_exists(link):
        if installation_mode == "full":
            findings.append(f"global link is missing: {link}")
        else:
            print("Global link: not configured (local mode)")
    else:
        source_checked = True
        try:
            global_dir = link.resolve(strict=True) if link.is_symlink() else link
        except OSError:
            global_dir = None
            findings.append(f"global link is broken or unreadable: {link}")
        if global_dir is not None and not global_dir.is_dir():
            findings.append(f"global source is not a directory: {global_dir}")
        elif global_dir is not None:
            try:
                source_data = source_manifest_from_global(global_dir)
                source_schema = int(source_data["schema_version"])
                print(f"Available source schema: {source_schema}")
                if source_schema != consumer_schema:
                    findings.append(
                        f"structural schema differs (installed {consumer_schema}, available {source_schema})"
                    )
            except RuntimeError as error:
                findings.append(str(error))
            source_checkout = source_checkout_for_global(global_dir)
            if source_checkout is None:
                findings.append("source checkout identity is unavailable; commit comparison could not be performed")
            else:
                try:
                    current_commit, current_url = source_identity(source_checkout)
                    print(f"Available source commit: {current_commit}")
                except RuntimeError as error:
                    findings.append(str(error))

    if current_commit is not None:
        if current_commit != base_commit:
            relation = source_commit_is_ancestor(source_checkout, base_commit, current_commit) if source_checkout else None
            if relation is True:
                findings.append("global source has advanced since this consumer was installed")
            elif relation is False:
                findings.append("recorded source commit differs and is not an ancestor of the available source")
            else:
                findings.append("recorded source commit differs; ancestry could not be determined")
    if source_checked:
        recorded_url = consumer.get("source_url")
        if current_url is not None and recorded_url != current_url:
            findings.append("recorded source URL differs from the available source URL")
        elif isinstance(recorded_url, str) and current_url is None:
            findings.append("recorded source URL cannot be compared because the available source has no remote URL")

    if findings:
        print("Status: attention required")
        for finding in findings:
            print(f"- {finding}")
        print("No files were changed. Review the structural-upgrade skill before making changes.")
        return 1

    print("Status: current")
    if installation_mode == "local" and not path_exists(link):
        print("Local mode is configured; source checkout comparison was skipped because no global link is expected.")
    else:
        print("No provenance or source-identity divergence was detected; consumer files were not inspected or changed.")
    return 0


def create_link(link: Path, destination: Path) -> None:
    if os.name != "nt":
        link.symlink_to(destination, target_is_directory=True)
        return
    try:
        link.symlink_to(destination, target_is_directory=True)
    except OSError:
        if not link.parent.is_dir():
            raise RuntimeError(f"Link parent directory does not exist: {link.parent}")
        command = subprocess.list2cmdline(["mklink", "/J", str(link), str(destination)])
        if subprocess.run(["cmd.exe", "/d", "/s", "/c", command], check=False).returncode:
            raise RuntimeError("Could not create a symlink or directory junction on Windows")


def install(target: Target, result: Preflight, mode: str) -> int:
    if result.signals:
        print_blocked(target, result)
        return 2
    if target.root.resolve() == result.source_root.resolve() and target.kind != "global":
        print_blocked(target, result)
        return 2
    if mode == "local" and path_exists(target.global_link):
        try:
            existing_is_source = (
                target.global_link.is_symlink()
                and target.global_link.resolve(strict=True)
                == (result.source_root / "global").resolve(strict=True)
            )
        except OSError:
            existing_is_source = False
        if not existing_is_source:
            print_blocked(
                target,
                Preflight(
                    (Signal(target.global_link, "existing global link requires review"),),
                    result.source_root,
                    result.source_commit,
                    result.source_url,
                ),
            )
            return 2
    if target.kind == "global" or mode == "global":
        if target.global_link.is_symlink():
            try:
                if target.global_link.resolve(strict=True) == (result.source_root / "global").resolve(strict=True):
                    print(f"Global link is already correct: {target.global_link}")
                    return 0
            except OSError:
                pass
        made_parent = not path_exists(target.global_link.parent)
        if made_parent:
            target.global_link.parent.mkdir(parents=True)
        create_link(target.global_link, result.source_root / "global")
        print(f"Local global link created: {target.global_link} -> {result.source_root / 'global'}")
        print("Ignore `.ai/global` before committing; the installer did not edit Git configuration or the index.")
        return 0

    template = result.source_root / ".ai/templates/project"
    created: list[Path] = []
    created_dirs: list[Path] = []
    try:
        dirs = {target.ai_dir / rel for rel in PROJECT_DIRECTORIES}
        dirs.update((target.root / rel).parent for rel in template_destinations(result.source_root))
        if mode == "full":
            dirs.add(target.ai_dir)
        preexisting_dirs = {
            ancestor
            for directory in dirs
            for ancestor in directory.parents
            if ancestor != target.root and path_exists(ancestor)
        }
        for directory in sorted(dirs, key=lambda p: len(p.parts)):
            if path_exists(directory):
                continue
            missing: list[Path] = []
            parent = directory
            while parent != target.root and not path_exists(parent):
                missing.append(parent)
                parent = parent.parent
            directory.mkdir(parents=True, exist_ok=False)
            created_dirs.extend(missing)

        agents = target.root / "AGENTS.md"
        if path_exists(agents):
            raise RuntimeError(f"Preflight mismatch: AGENTS.md became occupied: {agents}")
        agents.write_text((template / "AGENTS.md").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        created.append(agents)

        for source_file in sorted(template.rglob("*")):
            rel = source_file.relative_to(template)
            if not source_file.is_file() or source_file.name == ".gitkeep" or rel == Path("AGENTS.md"):
                continue
            destination = target.ai_dir / Path(*rel.parts[1:]) if rel.parts[0] == ".ai" else target.root / rel
            if path_exists(destination):
                raise RuntimeError(f"Preflight mismatch: destination became occupied: {destination}")
            if not path_exists(destination.parent):
                destination.parent.mkdir(parents=True, exist_ok=True)
                created_dirs.append(destination.parent)
            destination.write_text(source_file.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
            created.append(destination)

        if mode == "full":
            made_link_parent = not path_exists(target.global_link.parent)
            if made_link_parent:
                target.global_link.parent.mkdir(parents=True)
            create_link(target.global_link, result.source_root / "global")
            created.append(target.global_link)
            if made_link_parent:
                created_dirs.append(target.global_link.parent)
        manifest = {
            "format": CONSUMER_MANIFEST_FORMAT,
            "schema_version": SCHEMA_VERSION,
            "source_url": result.source_url,
            "base_commit": result.source_commit,
            "installation_mode": mode,
        }
        manifest_path = target.root / MANIFEST
        if not path_exists(manifest_path.parent):
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            created_dirs.append(manifest_path.parent)
        with manifest_path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(manifest, indent=2) + "\n")
        created.append(manifest_path)
    except Exception:
        for path in reversed(created):
            try:
                if path.is_symlink() or path.is_file():
                    path.unlink()
            except OSError:
                pass
        for path in sorted(set(created_dirs) | {parent for item in created for parent in item.parents}, key=lambda p: len(p.parts), reverse=True):
            if path == target.root:
                continue
            if path in preexisting_dirs:
                continue
            try:
                if path.is_dir() and not any(path.iterdir()):
                    path.rmdir()
            except OSError:
                pass
        raise

    print(f"Installation complete: {target.root}")
    print(f"Agent instructions: {target.root / 'AGENTS.md'}")
    if mode == "full":
        print(f"Local global link: {target.global_link} -> {result.source_root / 'global'}")
        print("Before committing, ignore `.ai/global` locally. The installer did not alter ignore files or the Git index.")
    print(f"Provenance: {target.root / MANIFEST}")
    return 0


def repair_link(target: Target, result: Preflight) -> int:
    link = target.global_link
    expected = result.source_root / "global"
    if path_exists(link) and not link.is_symlink():
        raise RuntimeError(f"Refusing to replace existing non-symlink global path: {link}")
    if path_exists(link.parent) and not link.parent.is_dir():
        raise RuntimeError(f"Agent context path is not a directory: {link.parent}")
    if link.is_symlink():
        try:
            if link.resolve(strict=True) == expected.resolve(strict=True):
                print(f"Global link is already correct: {link}")
                return 0
        except OSError:
            pass
        link.unlink()
    made_parent = not path_exists(link.parent)
    if made_parent:
        link.parent.mkdir(parents=True)
    create_link(link, expected)
    if made_parent:
        print(f"Created local context directory: {link.parent}")
    print(f"Repaired local global link: {link} -> {expected}")
    print("Ignore `.ai/global` before committing; Git files were not modified.")
    return 0


def init_mother() -> int:
    repository = source_root()
    link = repository / ".ai/global"
    relative = Path("..") / "global"
    if link.is_symlink() and os.readlink(link) == str(relative):
        print(f"Mother link is already correct: {link} -> {relative}")
        return 0
    raise RuntimeError(
        f"Mother link is missing or differs from the required tracked relative link: {link} -> {relative}. "
        "Create or repair it explicitly, inspect the result, and track it as normal repository content; "
        "the installer will not mutate its source checkout."
    )


def plan_mother() -> int:
    link = source_root() / ".ai/global"
    relative = Path("..") / "global"
    if link.is_symlink() and os.readlink(link) == str(relative):
        print(f"Mother link is already correct: {link} -> {relative}")
    elif path_exists(link):
        print(f"Mother link destination is occupied: {link}", file=sys.stderr)
        return 2
    else:
        print(f"Mother link is missing: {link} -> {relative}", file=sys.stderr)
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("plan", "status", "install", "repair-link"):
        child = sub.add_parser(command)
        child.add_argument("target", nargs="?", type=Path, help="project root, .ai directory, or exact .ai/global path")
        if command == "install":
            child.add_argument("--mode", choices=("full", "local", "global"), default="full")
            child.add_argument("--local", action="store_true", help="same as --mode local")
            child.add_argument("-y", "--yes", action="store_true", help="noninteractive compatibility; never bypasses preflight")
    sub.add_parser("plan-mother")
    sub.add_parser("init-mother")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "plan-mother":
            return plan_mother()
        if args.command == "init-mother":
            return init_mother()
        target = resolve_target(args.target, Path.cwd())
        if args.command == "status":
            return status(target)
        mode = "full"
        if args.command == "install":
            mode = "local" if args.local else args.mode
        elif target.kind == "global":
            mode = "global"
        result = preflight(target, "repair" if args.command == "repair-link" else mode)
        if args.command == "plan":
            print_plan(target, result)
            return 0
        if args.command == "install":
            return install(target, result, mode)
        return repair_link(target, result)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
