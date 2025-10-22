# tests/test_monthly_summary.py
"""
Test Module: test_monthly_summary.py
Purpose:
    - Validate monthly_summary.py for correct aggregation and summary calculations.
"""

import pytest
import pandas as pd
from src.monthly_summary import monthly_summary

def test_monthly_summary_structure(sample_csv_file):
    """Ensure summary output is a DataFrame with expected columns."""
    summary_df = monthly_summary(file_path=sample_csv_file)
    assert isinstance(summary_df, pd.DataFrame)
    expected_cols = {"Month", "Total"}
    assert expected_cols.issubset(summary_df.columns), "Missing expected summary columns"

def test_monthly_summary_values(sample_csv_file):
    """Ensure monthly totals are greater than zero."""
    summary_df = monthly_summary(file_path=sample_csv_file)
    assert  (summary_df["Total"] >= 0).all(), "Monthly totals must be non-negative"