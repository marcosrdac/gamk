#!/usr/bin/env python3
"""Probe the PowerShell wrappers through pwsh, including the NixOS path."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


def pwsh_prefix() -> list[str]:
    if shutil.which("pwsh") and shutil.which("python3"):
        return ["pwsh"]
    if shutil.which("nix"):
        return [
            "nix",
            "shell",
            "nixpkgs#powershell",
            "nixpkgs#python3",
            "--command",
            "pwsh",
        ]
    raise RuntimeError("pwsh is unavailable and Nix is not on PATH")


def run_pwsh(*arguments: object, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = [
        *pwsh_prefix(),
        "-NoLogo",
        "-NoProfile",
        "-NonInteractive",
        *(str(argument) for argument in arguments),
    ]
    result = subprocess.run(
        command,
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode:
        raise AssertionError(
            f"PowerShell command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def snapshot(root: Path) -> list[tuple[str, bool, str | None, bool]]:
    entries: list[tuple[str, bool, str | None, bool]] = []
    for path in root.rglob("*"):
        is_link = path.is_symlink()
        entries.append(
            (
                path.relative_to(root).as_posix(),
                is_link,
                os.readlink(path) if is_link else None,
                path.is_dir() if not is_link else False,
            )
        )
    return sorted(entries)


def assert_contains(result: subprocess.CompletedProcess[str], text: str) -> None:
    combined = result.stdout + result.stderr
    if text not in combined:
        raise AssertionError(f"Expected {text!r} in PowerShell output:\n{combined}")


def assert_exit(result: subprocess.CompletedProcess[str], code: int) -> None:
    if result.returncode != code:
        raise AssertionError(
            f"Expected exit code {code}, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def powershell_quote(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def main() -> int:
    install_wrapper = REPOSITORY / "scripts/install.ps1"
    copy_wrapper = REPOSITORY / "scripts/copy-install.ps1"

    parser_command = (
        "$ErrorActionPreference = 'Stop'; "
        f"$files = @({powershell_quote(install_wrapper)}, {powershell_quote(copy_wrapper)}); "
        "foreach ($file in $files) { "
        "$tokens = $null; $errors = $null; "
        "[System.Management.Automation.Language.Parser]::ParseFile($file, [ref]$tokens, [ref]$errors) | Out-Null; "
        "if ($errors.Count -gt 0) { throw \"Parse errors in $file\" }; "
        "Write-Output \"parse OK: $file\" }"
    )
    parsed = run_pwsh("-Command", parser_command)
    assert_contains(parsed, "parse OK")
    print("PowerShell parsing: OK")

    with tempfile.TemporaryDirectory(prefix="gamk-pwsh-") as temporary:
        workspace = Path(temporary)

        plan_target = workspace / "project with spaces"
        plan_target.mkdir()
        before = snapshot(plan_target)
        planned = run_pwsh("-File", install_wrapper, "plan", plan_target)
        assert_contains(planned, "No known migration signals")
        if snapshot(plan_target) != before:
            raise AssertionError("plan changed the target")
        print("install.ps1 plan with spaces: OK")

        install_target = workspace / "install target with spaces"
        install_target.mkdir()
        installed = run_pwsh("-File", install_wrapper, "install", install_target)
        link = install_target / ".ai" / "global"
        if not (install_target / "AGENTS.md").is_file():
            raise AssertionError("full install did not copy AGENTS.md")
        if not (install_target / ".ai" / "global-manifest.json").is_file():
            raise AssertionError("full install did not write provenance")
        if not link.is_symlink() or link.resolve() != (REPOSITORY / "global").resolve():
            raise AssertionError("full install did not create the expected Linux link")
        assert_contains(installed, "Installation complete")
        print("install.ps1 full install on Linux filesystem: OK")

        status = run_pwsh("-File", install_wrapper, "status", install_target)
        assert_contains(status, "Status: current")
        print("install.ps1 status: OK")

        blocked_target = workspace / "blocked target"
        blocked_target.mkdir()
        (blocked_target / "AGENTS.md").write_text("keep this\n", encoding="utf-8")
        before = snapshot(blocked_target)
        blocked = run_pwsh("-File", install_wrapper, "install", blocked_target, check=False)
        assert_exit(blocked, 2)
        assert_contains(blocked, "No files were changed")
        if snapshot(blocked_target) != before:
            raise AssertionError("blocked install changed the target")
        print("install.ps1 blocked install without mutation: OK")

        copy_target = workspace / "copy target with spaces"
        copied = run_pwsh("-File", copy_wrapper, copy_target)
        if not (copy_target / "AGENTS.md").is_file():
            raise AssertionError("copy install did not copy AGENTS.md")
        if not (copy_target / ".ai" / "work" / "doing").is_dir():
            raise AssertionError("copy install did not create the work directory")
        if (copy_target / ".ai" / "global-manifest.json").exists():
            raise AssertionError("copy install unexpectedly wrote provenance")
        assert_contains(copied, "Files copied")
        print("copy-install.ps1 clean install: OK")

        copy_blocked_target = workspace / "copy blocked"
        copy_blocked_target.mkdir()
        (copy_blocked_target / "AGENTS.md").write_text("owner instructions\n", encoding="utf-8")
        before = snapshot(copy_blocked_target)
        copy_blocked = run_pwsh("-File", copy_wrapper, copy_blocked_target, check=False)
        assert_exit(copy_blocked, 2)
        assert_contains(copy_blocked, "No files were copied")
        if snapshot(copy_blocked_target) != before:
            raise AssertionError("blocked copy install changed the target")
        print("copy-install.ps1 blocked install without mutation: OK")

    mother = run_pwsh("-File", install_wrapper, "plan-mother")
    assert_contains(mother, "Mother link is already correct")
    print("install.ps1 plan-mother: OK")
    print("All PowerShell/NixOS probes passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
