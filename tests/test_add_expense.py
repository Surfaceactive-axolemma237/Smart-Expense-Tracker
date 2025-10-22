# tests\test_add_expense.py
"""
Unit tests for add_expense.py module.
Ensures expense addition logic works correctly with sample data.

Test Module: test_add_expense.py
Purpose:
    - Validate add_expense.py module for data addition, input validation, and file handling.
"""

import pytest
import pandas as pd
from src.add_expense import add_expense

def test_add_expense_adds_entry(sample_csv_file):
    """Ensure add_module correctly adds a new row to the CSV."""
    initial_df = pd.read_csv(sample_csv_file)
    initial_len = len(initial_df)

    add_expense("2025-10-12", "Food", "Test Lunch", 250.0, file_path=sample_csv_file)

    updated_df = pd.read_csv(sample_csv_file)
    assert len(updated_df) == initial_len + 1, "Expense row should be added to CSV"

def test_add_expense_invalid_amount(sample_csv_file):
    """Ensure function handles invalid amount gracefully."""
    with pytest.raises(ValueError):
        add_expense("2025-10-12", "Transport", "Invalid Entry", -100, file_path=sample_csv_file)