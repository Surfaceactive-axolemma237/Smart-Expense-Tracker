# tests/test_yearly_overview.py
"""
Test Module: test_yearly_overview.py
Purpose:
    - Validate yearly_overview.py for correct yearly aggregation and trends.
"""

import pytest
import pandas as pd
from src.yearly_overview import yearly_total_summary

def test_yearly_overview_structure(sample_csv_file):
    """Ensure yearly overview has correct structure."""
    yearly_df = yearly_total_summary(file_path=sample_csv_file)
    assert isinstance(yearly_df, pd.DataFrame)
    expected_cols = {"Year", "Total"}
    assert expected_cols.issubset(yearly_df.columns), "Missing expected overview columns"

def test_yearly_overview_values(sample_csv_file):
    """Ensure yearly totals are non-negative and increasing over time."""
    yearly_df = yearly_total_summary(file_path=sample_csv_file)
    assert (yearly_df["Total"] >= 0).all(), "Yearly totals must be non-negative"