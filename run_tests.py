#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner and coverage analysis script
Supports various test modes and report generation
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_all_tests(verbose=True, coverage=False):
    """Run all tests"""
    cmd = ["pytest", "tests/", "-v" if verbose else ""]
    
    if coverage:
        cmd.extend(["--cov=components", "--cov-report=html", "--cov-report=term-missing"])
    
    cmd = [c for c in cmd if c]  # Remove empty strings
    
    print("Test runner - Running all tests...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_unit_tests(verbose=True):
    """Run unit tests only"""
    cmd = ["pytest", "tests/", "-m", "unit", "-v" if verbose else ""]
    cmd = [c for c in cmd if c]
    
    print("Test runner - Running unit tests...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_integration_tests(verbose=True):
    """Run integration tests only"""
    cmd = ["pytest", "tests/", "-m", "integration", "-v" if verbose else ""]
    cmd = [c for c in cmd if c]
    
    print("Test runner - Running integration tests...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_specific_test(test_name, verbose=True):
    """Run specific test"""
    cmd = ["pytest", f"tests/{test_name}", "-v" if verbose else ""]
    cmd = [c for c in cmd if c]
    
    print(f"Test runner - Running test: {test_name}")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def run_tests_with_coverage(verbose=True):
    """Run tests and generate coverage report"""
    cmd = [
        "pytest", "tests/",
        "--cov=components",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v" if verbose else ""
    ]
    cmd = [c for c in cmd if c]
    
    print("Test runner - Running tests and generating coverage report...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\nCoverage report generated:")
        print("   HTML Report: htmlcov/index.html")
    
    return result.returncode


def list_available_tests():
    """List all available tests"""
    cmd = ["pytest", "tests/", "--collect-only", "-q"]
    
    print("Available tests:\n")
    subprocess.run(cmd)


def run_failed_tests_only():
    """Run only previously failed tests"""
    cmd = ["pytest", "tests/", "--lf", "-v"]
    
    print("Test runner - Running previously failed tests...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="FileGather Pro Test Runner")
    
    parser.add_argument(
        "mode",
        nargs="?",
        default="all",
        choices=["all", "unit", "integration", "coverage", "failed", "list"],
        help="Test execution mode"
    )
    
    parser.add_argument(
        "--test",
        type=str,
        help="Run specific test file (e.g., test_search_logic.py)"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode (less output)"
    )
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    try:
        if args.test:
            returncode = run_specific_test(args.test, verbose)
        elif args.mode == "all":
            returncode = run_all_tests(verbose)
        elif args.mode == "unit":
            returncode = run_unit_tests(verbose)
        elif args.mode == "integration":
            returncode = run_integration_tests(verbose)
        elif args.mode == "coverage":
            returncode = run_tests_with_coverage(verbose)
        elif args.mode == "failed":
            returncode = run_failed_tests_only()
        elif args.mode == "list":
            list_available_tests()
            returncode = 0
        
        if returncode == 0:
            print("\nAll tests passed!")
        else:
            print(f"\nTests failed (return code: {returncode})")
        
        sys.exit(returncode)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
