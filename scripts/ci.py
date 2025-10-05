#!/usr/bin/env python3
"""
Local CI runner: replicate the main steps from .github/workflows/ci.yml so you can run them locally.

Usage examples:
  python -m scripts.ci all        # run format check, lint, tests, coverage, pip-audit
  python -m scripts.ci test       # run pytest with coverage
  python -m scripts.ci lint       # run pylint
  python -m scripts.ci format     # run black --check .
  python -m scripts.ci audit      # run pip-audit on requirements.txt

Notes:
- Ensure required tools are installed: pip install -r requirements.txt && pip install black pylint pytest pytest-cov pip-audit
- This script is cross-platform (Windows/Linux/macOS) and uses Python's subprocess.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str] | str, check: bool = True, timeout: float | None = None) -> int:
    print(f"\n$ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(cmd, cwd=REPO_ROOT, check=check, timeout=timeout)
        return result.returncode
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return 124  # common timeout exit code
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        if check:
            raise
        return e.returncode


def ensure_tool(name: str) -> None:
    if shutil.which(name) is None:
        print(f"ERROR: Required tool '{name}' not found on PATH. Please install it.")
        print("       For example: pip install black pylint pytest pytest-cov pip-audit")
        sys.exit(1)


def step_format() -> int:
    ensure_tool("black")
    return run([sys.executable, "-m", "black", "--check", "."], check=False)


def step_lint() -> int:
    ensure_tool("pylint")
    rcfile = ".pylintrc"
    if (REPO_ROOT / rcfile).exists():
        return run([sys.executable, "-m", "pylint", f"--rcfile={rcfile}", "."], check=False)
    return run([sys.executable, "-m", "pylint", "."], check=False)


def step_test() -> int:
    ensure_tool("pytest")
    # Options are centralized in pyproject.toml [tool.pytest.ini_options]
    # Add a hard timeout to prevent hangs (10 minutes)
    return run([
        sys.executable,
        "-m",
        "pytest",
    ], check=False, timeout=600)


def step_audit() -> int:
    ensure_tool("pip-audit")
    req = REPO_ROOT / "requirements.txt"
    if req.exists():
        return run([sys.executable, "-m", "pip_audit", "-r", str(req), "--timeout", "60"], check=False, timeout=180)
    # Fallback: audit current environment
    return run([sys.executable, "-m", "pip_audit", "--timeout", "60"], check=False, timeout=180)




def step_all() -> int:
    codes = [
        ("format", step_format()),
        ("lint", step_lint()),
        ("test", step_test()),
        ("audit", step_audit()),
    ]
    print("\nSummary:")
    failed = False
    for name, code in codes:
        status = "OK" if code == 0 else f"FAIL({code})"
        print(f"  {name:8}: {status}")
        if code != 0:
            failed = True
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local CI tasks")
    parser.add_argument(
        "task",
        choices=["all", "test", "lint", "format", "audit"],
        help="Which task to run",
    )
    args = parser.parse_args(argv)

    tasks = {
        "all": step_all,
        "test": step_test,
        "lint": step_lint,
        "format": step_format,
        "audit": step_audit,
    }
    return tasks[args.task]()


if __name__ == "__main__":
    raise SystemExit(main())
