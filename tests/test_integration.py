# tests/test_integration.py
"""
Central test runner for Smart Expense Tracker.
Executes all unit tests (like a BIOS pre-check) before app startup.

Integration Test Runner - test_integration.py
Purpose:
    - Run all tests automatically (like a BIOS self-check)
    - Log results for diagnostics
"""

import pytest
from datetime import datetime
from pathlib import Path

def run_all_tests():
    """Runs all pytest tests and logs output."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"test_report_{timestamp}.txt"

    with open(log_file, "w", encoding="utf-8") as log:
        result = pytest.main(["-v", "tests", "--tb=short"])

    print(f"\n🧩 Test Report saved to: {log_file}")
    if result == 0:
        print("✅ All tests passed successfully!")
    else:
        print("⚠️ Some tests failed. Check the log file for details.")

if __name__ == "__main__":
    run_all_tests()