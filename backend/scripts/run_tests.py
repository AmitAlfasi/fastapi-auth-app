#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add backend/app to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "backend"))

def run_tests(verbose=True, coverage=False, test_path=None):
    """
    Run pytest with specified options
    """
    cmd = ["pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend([
            "--cov=backend/app",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])

    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("backend/tests/")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run FastAPI backend tests")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run tests quietly")
    parser.add_argument("-c", "--coverage", action="store_true", help="Include coverage report")
    parser.add_argument("-p", "--path", help="Path to specific test file or folder")

    args = parser.parse_args()

    if args.coverage:
        try:
            import pytest_cov
        except ImportError:
            print("pytest-cov is required for coverage. Install it with: pip install pytest-cov")
            sys.exit(1)

    run_tests(
        verbose=not args.quiet,
        coverage=args.coverage,
        test_path=args.path
    )

if __name__ == "__main__":
    main()
