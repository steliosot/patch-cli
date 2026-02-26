#!/bin/bash

# Quick Test Runner for patch.py
# Runs all tests with a simple output

echo "🧪 Running patch.py tests..."
echo ""

# Run unit tests
echo "=== Unit Tests ==="
python3 test_unit.py 2>&1 | tail -5
echo ""

# Run integration tests
echo "=== Integration Tests ==="
python3 test_integration.py 2>&1 | tail -5
echo ""

# Run scenario tests
echo "=== Scenario Tests ==="
python3 test_scenarios.py 2>&1 | tail -5
echo ""

echo "=== Summary ==="
echo "All tests completed!"
echo "See TEST_REPORT.md for detailed results"