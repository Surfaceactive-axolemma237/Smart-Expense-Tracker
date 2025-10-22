# src/category_insight.py
"""
Module: category_insight
------------------------
Analyzes spending by category across all recorded expenses.

Structure:
    1. category_insight()               → Core logic (pure/testable)
    2. category_insight_interactive()   → CLI display wrapper

Compatible with both CLI execution and pytest-based modular testing.
"""


import pandas as pd
from pathlib import Path
from tabulate import tabulate
from src.data_manager import ensure_csv_exists
from src.config import DATA_FILE


# ------------------------------------------------------------------------
# 🧠 PURE FUNCTION (Used in testing & backend)
# ------------------------------------------------------------------------
def category_insight(file_path: str | Path = DATA_FILE) -> pd.DataFrame:
    """
    Generate insights on spending by category: total & average per category.

    Args:
        file_path (str | Path): Path to the expense CSV file.

    Returns:
        pd.DataFrame: DataFrame with columns ['Category', 'Entries', 'Total Spent', 'Average Spent'].
                      Returns empty DataFrame if no valid expense data is found.
    """
    file_path = Path(file_path)
    ensure_csv_exists()

    df = pd.read_csv(file_path)

    # Handle empty or missing columns
    if df.empty or "Category" not in df.columns or "Amount" not in df.columns:
        return pd.DataFrame(columns=["Category", "Entries", "Total Spent", "Average Spent"])
    

    # Convert Amount Safely
    df["Amount"] =  pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    # Drop rows without category
    df = df.dropna(subset=["Category"])
    if df.empty:
        return pd.DataFrame(columns=["Category", "Entries", "Total Spent", "Average Spent"])
    
    # Group and aggregate
    insight_df = (
        df.groupby("Category", as_index=False)["Amount"]
        .agg(["sum", "mean", "count"])
        .reset_index()
        .rename(columns={"sum": "Total Spent", "mean": "Average Spent", "count": "Entries"})
    )


    # Clip to avoid negatives (in case of invalid entries)
    insight_df["Total Spent"] = insight_df["Total Spent"].clip(lower=0)
    insight_df["Average Spent"] = insight_df["Average Spent"].clip(lower=0)

    # Sort descending by total spent
    insight_df = insight_df.sort_values("Total Spent", ascending=False).reset_index(drop=True)

    return insight_df[["Category", "Entries", "Total Spent", "Average Spent"]]


# ------------------------------------------------------------------------
# 💬 CLI DISPLAY WRAPPER
# ------------------------------------------------------------------------
def category_insight_interactive(file_path: str | Path = DATA_FILE):
    """
    Interactive CLI view for category insights.
    Prints formatted table and totals.
    """
    insight_df = category_insight(file_path)

    if insight_df.empty:
        print("⚠️ No expense data available for category insights.")
        return

    print("\n📊 Category Insight Summary")
    print(tabulate(insight_df, headers="keys", showindex=False, tablefmt="grid", floatfmt=".2f"))

    total_spent = insight_df["Total Spent"].sum()
    avg_spent = insight_df["Average Spent"].mean()
    print(f"\n💰 Overall Total Spent: ₹{total_spent:.2f}")
    print(f"📈 Average Spending Across Categories: ₹{avg_spent:.2f}")


# ------------------------------------------------------------------------
# 🧪 STANDALONE EXECUTION
# ------------------------------------------------------------------------
if __name__ == "__main__":
    category_insight_interactive()