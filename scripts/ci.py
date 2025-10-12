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
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VENV_DIRS = [REPO_ROOT / ".venv", REPO_ROOT / "venv"]


def compute_requirements_hash(req_path: Path) -> str:
    """Return a sha256 hex digest of the requirements file contents; empty string if missing."""
    try:
        data = req_path.read_bytes()
    except FileNotFoundError:
        return ""
    return hashlib.sha256(data).hexdigest()


def create_venv(venv_path: Path) -> None:
    """Create a virtual environment at venv_path using the current Python interpreter."""
    print(f"Creating virtualenv at {venv_path}")
    run([sys.executable, "-m", "venv", str(venv_path)], check=True)


def install_requirements_into_venv(python_exe: str, req_file: Path) -> int:
    """Install/upgrade requirements into the given python executable's environment."""
    if not req_file.exists():
        print(f"No requirements file found at {req_file}; skipping pip install")
        return 0
    print(f"Installing/Upgrading requirements into venv using {python_exe}")
    return run([python_exe, "-m", "pip", "install", "--upgrade", "-r", str(req_file)], check=True)


def install_playwright_browsers(python_exe: str) -> int:
    """Install Playwright browser binaries if playwright is available."""
    try:
        # Check if playwright is installed
        result = subprocess.run(
            [python_exe, "-c", "import playwright"], capture_output=True, text=True, cwd=REPO_ROOT, check=False
        )
        if result.returncode != 0:
            print("Playwright not installed; skipping browser installation")
            return 0

        print("Installing Playwright browsers...")
        return run([python_exe, "-m", "playwright", "install"], check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Warning: Failed to install Playwright browsers: {exc}")
        return 0


def get_python_executable() -> str:
    """Return the project's virtualenv Python if present, else sys.executable.

    Looks for common venv dirs: .venv, venv. On Windows uses Scripts/python.exe,
    on Unix uses bin/python.
    """
    candidates = [REPO_ROOT / ".venv", REPO_ROOT / "venv"]
    for cand in candidates:
        if cand.exists() and cand.is_dir():
            # Windows
            py_win = cand / "Scripts" / "python.exe"
            py_unix = cand / "bin" / "python"
            if py_win.exists():
                return str(py_win)
            if py_unix.exists():
                return str(py_unix)
    # Fallback to current interpreter
    return sys.executable


def run(cmd: list[str] | str, check: bool = True, timeout: float | None = None) -> int:
    print(f"\n$ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        # If caller passed a list, run it directly. Otherwise pass the string to shell.
        result = subprocess.run(cmd, cwd=REPO_ROOT, check=check, timeout=timeout)
        return result.returncode
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return 124  # common timeout exit code
    except subprocess.CalledProcessError as ex:
        print(f"Command failed with exit code {ex.returncode}")
        if check:
            raise
        return ex.returncode


def ensure_tool(name: str) -> None:
    """Ensure a tool is available either as an executable on PATH or as an importable module in the venv.

    Examples: 'black', 'pylint', 'pytest', 'pip-audit'. For module check, hyphens are replaced
    with underscores (pip-audit -> pip_audit) when attempting import.
    """
    # First try PATH
    if shutil.which(name) is not None:
        return
    # Next try importing the module using the selected python executable
    module = name.replace("-", "_")
    try:
        # Use the project's python executable (if available) to attempt import
        result = subprocess.run([get_python_executable(), "-c", f"import {module}"], cwd=REPO_ROOT, check=False)
        if result.returncode == 0:
            return
    except (OSError, subprocess.SubprocessError) as exc:
        # If subprocess fails to start or runs into an internal error, treat as not available
        _ = exc  # avoid unused variable in some linters
    print(f"ERROR: Required tool '{name}' not found on PATH nor importable by {get_python_executable()}. Please install it.")
    print("       For example: pip install -r requirements.txt")
    sys.exit(1)


def step_format() -> int:
    ensure_tool("black")
    return run([PYTHON, "-m", "black", "--check", "."], check=False)


def step_lint() -> int:
    ensure_tool("pylint")
    rcfile = ".pylintrc"
    # Lint only specific source directories instead of the entire project
    source_dirs = ["src", "scripts", "tests", "bdd"]
    existing_dirs = [d for d in source_dirs if (REPO_ROOT / d).exists()]

    if not existing_dirs:
        print("No source directories found to lint")
        return 0

    if (REPO_ROOT / rcfile).exists():
        return run([PYTHON, "-m", "pylint", f"--rcfile={rcfile}"] + existing_dirs, check=False)
    return run([PYTHON, "-m", "pylint"] + existing_dirs, check=False)


def run_pytest_suite(suite_name: str, suite_path: str) -> int:
    """Run a pytest suite using its dedicated pytest.ini configuration file.

    Args:
        suite_name: Human-readable name for the test suite (for logging)
        suite_path: Path to the test suite directory containing pytest.ini
    """
    ensure_tool("pytest")
    config_file = f"{suite_path}/pytest.ini"
    print(f"Running {suite_name} tests using {config_file}")
    return run([PYTHON, "-m", "pytest", "-c", config_file, suite_path], check=False, timeout=600)


def step_test() -> int:
    """Run unit tests with coverage."""
    return run_pytest_suite("unit", "tests")


def step_bdd() -> int:
    """Run BDD scenarios without coverage."""
    return run_pytest_suite("BDD", "bdd")


def step_audit() -> int:
    ensure_tool("pip-audit")
    req = REPO_ROOT / "requirements.txt"
    if req.exists():
        return run(
            [PYTHON, "-m", "pip_audit", "-r", str(req), "--timeout", "60"],
            check=False,
            timeout=180,
        )
    # Fallback: audit current environment
    return run([PYTHON, "-m", "pip_audit", "--timeout", "60"], check=False, timeout=180)


def step_update_venv() -> int:
    """Create or update the project virtualenv and install requirements, then exit with 0 on success."""
    try:
        ensure_venv_and_deps(force_update=True)
        return 0
    except (OSError, subprocess.CalledProcessError, subprocess.SubprocessError) as ex:
        print(f"Failed to update venv: {ex}")
        return 1


def step_all() -> int:
    codes = [
        ("format", step_format()),
        ("lint", step_lint()),
        ("test", step_test()),
        ("bdd", step_bdd()),
        ("audit", step_audit()),
    ]
    print("\n--- Summary ---")
    failed = False
    for name, code in codes:
        status = "OK" if code == 0 else f"FAIL({code})"
        print(f"  {name:8}: {status}")
        if code != 0:
            failed = True
    return 1 if failed else 0


def find_existing_venv() -> Path | None:
    for candidate in VENV_DIRS:
        if candidate.exists() and candidate.is_dir():
            # Heuristic: check for python executable inside
            if (candidate / "Scripts" / "python.exe").exists() or (candidate / "bin" / "python").exists():
                return candidate
    return None


def _compute_requirements_hash(req: Path, req_dev: Path) -> str:
    """Return sha256 of concatenated requirements files, empty string if none present."""
    try:
        data = b""
        if req.exists():
            data += req.read_bytes()
        if req_dev.exists():
            data += b"\n" + req_dev.read_bytes()
        if data:
            return hashlib.sha256(data).hexdigest()
    except OSError:
        return ""
    return ""


def _write_hash_file(hash_file: Path, current_hash: str) -> bool:
    """Write the requirements hash to file, return True on success."""
    try:
        hash_file.write_text(current_hash, encoding="utf-8")
        return True
    except OSError as exc:
        print(f"Warning: failed to write requirements hash file: {exc}")
        return False


def ensure_venv_and_deps(force_update: bool = False) -> None:
    """Ensure a project venv exists and dependencies from requirements.txt are installed/upgraded.

    Behavior:
    - If no venv exists, create `.venv` and install requirements.
    - If venv exists, compute hash of `requirements.txt` and `requirements-dev.txt` (if present) and compare with
      stored hash at `.venv/.requirements_hash`; if different or `force_update` is True,
      run pip install --upgrade -r requirements.txt and (if present) -r requirements-dev.txt,
      then update the stored hash.
    """
    req = REPO_ROOT / "requirements.txt"
    req_dev = REPO_ROOT / "requirements-dev.txt"
    venv = find_existing_venv()
    target_venv = REPO_ROOT / ".venv"

    # Decide whether to create venv
    if venv is None:
        create_venv(target_venv)
        venv = target_venv

    # Recompute python executable to point to venv python
    python_exe = get_python_executable()

    # Compute hash over requirements.txt and requirements-dev.txt (if exists)
    current_hash = _compute_requirements_hash(req, req_dev)

    hash_file = venv / ".requirements_hash"
    stored_hash = ""
    if hash_file.exists():
        try:
            stored_hash = hash_file.read_text(encoding="utf-8").strip()
        except OSError:
            stored_hash = ""

    if force_update or (current_hash and current_hash != stored_hash):
        print("Requirements changed or venv missing packages; installing/upgrading...")
        # Always install requirements.txt first if present
        return_code = 0
        if req.exists():
            return_code = install_requirements_into_venv(python_exe, req)
        # Then install dev requirements if present
        if return_code == 0 and req_dev.exists():
            return_code = install_requirements_into_venv(python_exe, req_dev)

        # Install Playwright browsers after requirements are installed
        if return_code == 0:
            install_playwright_browsers(python_exe)

        if return_code == 0:
            # write the combined hash
            _write_hash_file(hash_file, current_hash)
        else:
            print("Warning: pip install returned non-zero exit code")
    else:
        print("Venv exists and requirements appear up-to-date; skipping pip install")


# Prefer venv python when running modules so tests/tools run inside the project's venv
PYTHON = get_python_executable()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local CI tasks")
    parser.add_argument(
        "task",
        choices=["all", "test", "lint", "format", "audit", "bdd", "update-venv"],
        help="Which task to run",
    )
    parser.add_argument(
        "--update-venv", action="store_true", help="Force create/update the project venv and install requirements"
    )
    args = parser.parse_args(argv)

    # Ensure venv and dependencies are present/updated when requested or by default
    if args.update_venv:
        ensure_venv_and_deps(force_update=True)
    else:
        # Try best-effort to ensure venv exists and install only when requirements changed
        ensure_venv_and_deps()

    tasks = {
        "all": step_all,
        "test": step_test,
        "lint": step_lint,
        "format": step_format,
        "audit": step_audit,
        "bdd": step_bdd,
        "update-venv": step_update_venv,
    }
    return tasks[args.task]()


if __name__ == "__main__":
    raise SystemExit(main())
