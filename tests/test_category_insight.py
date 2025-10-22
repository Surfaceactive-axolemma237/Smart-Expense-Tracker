# tests/test_category_insight.py
"""
Test Module: test_category_insight.py
Purpose:
    - Validate category_insight.py for accurate category-wise aggregations.
"""

import pytest
import pandas as pd
from src.category_insight import category_insight

def test_category_insights_structure(sample_csv_file):
    """Ensure insights output DataFrame has required columns."""
    insight_df = category_insight(file_path=sample_csv_file)
    assert isinstance(insight_df, pd.DataFrame)
    expected_cols = {"Category", "Total Spent", "Average Spent"}
    assert expected_cols.issubset(insight_df.columns), "Missing expected insight columns"

def test_category_insights_non_negative(sample_csv_file):
    """Ensure category totals are non-negative."""
    insight_df = category_insight(file_path=sample_csv_file)
    assert (insight_df["Total Spent"] >= 0).all(), "Category totals must be non-negative"