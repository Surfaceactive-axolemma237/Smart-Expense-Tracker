# tests/test_view_expenses.py
"""
Unit tests for view_expenses.py module.
----------------------------------------
Verifies expense listing, sorting, and filtering logic.

Phase 3 Alignment:
    ✅ Uses get_expenses_df() (pure, testable function)
    ❌ Removes dependency on interactive CLI functions
"""

import pytest
import pandas as pd
from src.view_expenses import get_expenses_df


def test_list_expenses_return_df(sample_csv_file):
    """
    Ensure get_expenses_df() returns a valid non-empty DataFrame.
    """
    df = get_expenses_df(file_path=sample_csv_file)
    assert isinstance(df, pd.DataFrame), "Function should return a pandas DataFrame"
    assert not df.empty, "Returned DataFrame should not be empty"
    expected_columns = {"Date", "Category", "Description", "Amount"}
    assert expected_columns.issubset(df.columns), "Missing one or more expected columns"


def test_filter_expenses_by_category(sample_csv_file):
    """
    Ensure filtering by category returns expected rows only.
    """
    df = get_expenses_df(category="Food", file_path=sample_csv_file)
    assert not df.empty, "Filtered data should not be empty"
    assert all(df["Category"] == "Food"), "Filter should return only Food category expenses"


def test_sort_expenses_by_amount_descending(sample_csv_file):
    """
    Ensure sorting by Amount in descending order works correctly.
    """
    df = get_expenses_df(sort_by="Amount", descending=True, file_path=sample_csv_file)
    assert not df.empty, "DataFrame should not be empty"
    assert df["Amount"].is_monotonic_decreasing, "Amounts should be sorted descending"
