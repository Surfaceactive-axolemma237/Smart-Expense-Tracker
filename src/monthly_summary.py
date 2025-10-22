# src/monthly_summary.py
"""
Module: monthly_summary
-----------------------

Generates a monthly summary of total expenses grouped by month.

Structure:
    1. monthly_summary() → Core logic (pure/testable)
    2. monthly_summary_interactive() → CLI display wrapper

Compatible with CLI app and unit testing.
"""


import pandas as pd
from pathlib import Path
from tabulate import tabulate
from src.config import DATA_FILE
from src.data_manager import ensure_csv_exists


# ----------------------------------------------------------------------------------------------------
# 🧠 PURE FUNCTION (Testable Core)
# ----------------------------------------------------------------------------------------------------
def monthly_summary(file_path: str | Path = DATA_FILE) -> pd.DataFrame:
    """
    Generate a monthly summary of total expenses.

    Args:
        file_path (str | Path): Path to the CSV file containing expenses.

    Returns:
        pd.DataFrame: DataFrame with columns ['Month', 'Total'].
                      Returns an empty DataFrame if no valid data is found.
    """
    file_path = Path(file_path)
    ensure_csv_exists()

    df = pd.read_csv(file_path)

    # Handle empty CSV file
    if df.empty or "Date" not in df.columns or "Amount" not in df.columns:
        return pd.DataFrame(columns=["Month", "Total"])
    
    # Convert data types safely
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df['Amount'], errors="coerce").fillna(0)

    # Drop Invalid Dates
    df = df.dropna(subset=["Date"])
    if df.empty:
        return pd.DataFrame(columns=["Month", "Total"])
    
    # Extract Month
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # Aggregate totals
    summary_df = (
        df.groupby("Month", as_index=False)["Amount"]
        .sum()
        .rename(columns={"Amount": "Total"})
        .sort_values("Month")
        .reset_index(drop=True)
    )

    return summary_df


# ----------------------------------------------------------------------------------------------------
# 💬 CLI DISPLAY WRAPPER (Used in main.py)
# ----------------------------------------------------------------------------------------------------
def monthly_summary_interactive(file_path: str | Path = DATA_FILE):
    """
    Interactive CLI display for monthly summary.
    Prints a formatted table and total.
    """
    summary_df = monthly_summary(file_path)

    if summary_df.empty:
        print("⚠️ No expense data available for monthly summary.")
        return
    
    print("\n📅 Monthly Expense Summary")
    print(tabulate(summary_df, headers="keys", showindex=False, tablefmt="grid", floatfmt=".2f"))

    total_sum = summary_df["Total"].sum()
    print(f"\n💰 Total across all months: ₹{total_sum:.2f}")


# ----------------------------------------------------------------------------------------------------
# 🧪 Standalone Execution
# ----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    monthly_summary_interactive()