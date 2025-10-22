# tests\utils.py
"""
Utility functions for testing the Smart Expense Tracker.

This module provides:
    - Temporary CSV generator with sample expense data.
    - Timestamped logging for test reports.
    - Helper methods for future diagnostics integration.

Author: Varun Wagle
Version 2.0
Utility module for test helpers and fixtures.
"""

import tempfile
from pathlib import Path
import pytest
import csv
import os
from datetime import datetime, timedelta
import random

# ---------------------------------------------------------------------------------------
# Create sample CSV data for testing
# ---------------------------------------------------------------------------------------
def create_sample_csv(file_path):
    """
    Create a temporary CSV file with sample expense data.

    Returns:
        str: Path to the temporary CSV file.
    Generate a small sample CSV with consistent columns
    """
    headers = ["Date", "Category", "Description", "Amount"]
    categories = ["Food", "Transport", "Shopping", "Utilities", "Entertainment"]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        base_date = datetime.now()

        for i in range(10):
            writer.writerow([
                (base_date -timedelta(days=i * 3)).strftime("%Y-%m-%d"),
                random.choice(categories),
                f"Sample expense {i + 1}",
                round(random.uniform(50, 5000), 2)
            ])

@pytest.fixture
def sample_csv_file():
    """Fixture: Create temporary CSV and cleans up automatically."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        create_sample_csv(tmp.name)
        yield tmp.name
    Path(tmp.name).unlink(missing_ok=True)