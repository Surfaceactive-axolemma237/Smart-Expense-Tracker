# tests/test_visualization.py
"""
Test Module: test_visualization.py
Purpose:
    - Validate visualization.py for chart generation without errors.
    - Focus on ensuring plotting functions execute successfully.
"""
import pytest
import matplotlib
matplotlib.use("Agg") # Use non-GUI backend for tests

from src.visualization import (
    plot_monthly_spending,
    plot_monthly_spending_by_category,
    plot_category_breakdown,
    plot_spending_trend,
    plot_category_heatmap,
    plot_daily_distribution,
)

def test_plot_monthly_totals(sample_csv_file):
    """Ensure monthly bar chart executes without exception."""
    plot_monthly_spending(file_path=sample_csv_file)

def test_plot_category_bar(sample_csv_file):
    """Ensure category-wise bar chart executes without exception."""
    plot_monthly_spending_by_category(file_path=sample_csv_file)

def test_plot_category_pie(sample_csv_file):
    """Ensure pie chart executes without exception."""
    plot_category_breakdown(file_path=sample_csv_file)

def test_plot_trend_line(sample_csv_file):
    """Ensure trend line chart executes without exception."""
    plot_spending_trend(file_path=sample_csv_file)

def test_plot_heat_map(sample_csv_file):
    """Ensure heat map executes without exception."""
    plot_category_heatmap(file_path=sample_csv_file)

def test_plot_top5_expenses(sample_csv_file):
    """Ensure Top 5 Expenses chart executes without exception."""
    plot_daily_distribution(file_path=sample_csv_file)