#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

def run_tests(verbose=True, coverage=False, test_path=None):
    """
    Run pytest with specified options
    
    Args:
        verbose (bool): Whether to run in verbose mode
        coverage (bool): Whether to generate coverage report
        test_path (str): Specific test path to run (None for all tests)
    """
    # Base command
    cmd = ["pytest"]
    
    # Add verbose flag if requested
    if verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if coverage:
        cmd.extend([
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    # Add specific test path if provided
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # Run the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run FastAPI authentication tests")
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Run tests in quiet mode (no verbose output)"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "-p", "--path",
        help="Run specific test file or directory"
    )
    
    args = parser.parse_args()
    
    # Check if pytest-cov is installed when coverage is requested
    if args.coverage:
        try:
            import pytest_cov
        except ImportError:
            print("Error: pytest-cov is not installed. Install it with:")
            print("pip install pytest-cov")
            sys.exit(1)
    
    run_tests(
        verbose=not args.quiet,
        coverage=args.coverage,
        test_path=args.path
    )

if __name__ == "__main__":
    main() 