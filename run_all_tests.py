#!/usr/bin/env python3
"""
Comprehensive test runner for patch.py
Runs all test suites and provides a detailed report
"""

import sys
import os
import subprocess
import time


def run_test_file(test_file, name):
    """Run a test file and return results."""
    print(f"\n" + "=" * 60)
    print(f"   Running {name}")
    print("=" * 60)

    start_time = time.time()
    result = subprocess.run(
        ['python3', test_file],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    end_time = time.time()

    duration = end_time - start_time
    output = result.stdout + result.stderr

    # Extract test statistics
    lines = output.split('\n')
    stats = {
        'tests_run': 0,
        'failures': 0,
        'errors': 0,
        'success': result.returncode == 0
    }

    for line in lines:
        if 'Tests run:' in line or 'Ran' in line and 'test' in line:
            parts = line.split()
            if 'Tests run:' in line:
                for i, part in enumerate(parts):
                    if part == 'run:':
                        stats['tests_run'] = int(parts[i+1])
                    if part == 'Failures:':
                        stats['failures'] = int(parts[i+1])
                    if part == 'Errors:':
                        stats['errors'] = int(parts[i+1])
                        break

    # Count [✓] marks as individual test successes
    success_count = output.count('[✓]')
    failed_tests = output.count('ERROR:') + output.count('FAIL:')

    print(f"\nResults:")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Tests Run: {stats['tests_run']}")
    print(f"  Successes: {stats['tests_run'] - stats['failures'] - stats['errors']}")
    print(f"  Failures: {stats['failures']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Overall: {'PASSED ✓' if result.returncode == 0 else 'FAILED ✗'}")

    return stats


def main():
    """Run all tests and provide comprehensive report."""
    print("\n" + "=" * 60)
    print("   Patch.py - Comprehensive Test Suite")
    print("=" * 60)
    print(f"   Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    tests = [
        ('test_unit.py', 'Unit Tests'),
        ('test_integration.py', 'Integration Tests'),
        ('test_scenarios.py', 'Scenario-Based Tests'),
    ]

    total_stats = {
        'tests_run': 0,
        'failures': 0,
        'errors': 0,
        'failed_suites': 0
    }

    for test_file, name in tests:
        if not os.path.exists(test_file):
            print(f"\n[!] Test file not found: {test_file}")
            continue

        stats = run_test_file(test_file, name)

        total_stats['tests_run'] += stats['tests_run']
        total_stats['failures'] += stats['failures']
        total_stats['errors'] += stats['errors']

        if not stats['success']:
            total_stats['failed_suites'] += 1

    # Print comprehensive summary
    print("\n" + "=" * 60)
    print("   Overall Test Summary")
    print("=" * 60)
    print(f"\nTotal Tests Run: {total_stats['tests_run']}")
    print(f"Total Successes: {total_stats['tests_run'] - total_stats['failures'] - total_stats['errors']}")
    print(f"Total Failures: {total_stats['failures']}")
    print(f"Total Errors: {total_stats['errors']}")
    print(f"Failed Test Suites: {total_stats['failed_suites']}/{len(tests)}")

    success_rate = ((total_stats['tests_run'] - total_stats['failures'] - total_stats['errors']) / total_stats['tests_run'] * 100) if total_stats['tests_run'] > 0 else 0

    print(f"Success Rate: {success_rate:.1f}%")

    if total_stats['failures'] == 0 and total_stats['errors'] == 0:
        print(f"\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n✗ SOME TESTS FAILED")

    print("=" * 60 + "\n")

    return total_stats['failures'] == 0 and total_stats['errors'] == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)