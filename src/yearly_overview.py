# src/yearly_overview.py
"""
Module: yearly_overview
------------------------
Generates a summarized view of total expenses by year and by month.

Structure:
    1. yearly_overview()           → Month-wise summary (pure, testable)
    2. yearly_total_summary()      → Yearly aggregation (used in tests)
    3. yearly_overview_interactive() → CLI display wrapper

Fully modular for integration testing and standalone CLI use.
"""


import pandas as pd
from pathlib import Path
from tabulate import tabulate
from src.config import DATA_FILE
from src.data_manager import ensure_csv_exists


# ----------------------------------------------------------------------------------------------------
# 🧠 PURE FUNCTION (Detailed: Year + Month)
# ----------------------------------------------------------------------------------------------------
def yearly_overview(file_path: str | Path = DATA_FILE) -> pd.DataFrame:
    """
    Summarize total yearly expenses and monthly breakdowns.

    Args:
        file_path (str | Path): Path to the CSV data file.

    Return:
        pd.DataFrame: DataFrame with columns ['Year', 'Month', 'Total'].
                      Returns an empty DataFrame if data is missing or invalid.
    """
    file_path = Path(file_path)
    ensure_csv_exists()

    df = pd.read_csv(file_path)


    # ---- Validate Data ----
    if df.empty or "Date" not in df.columns or "Amount" not in df.columns:
        return pd.DataFrame(columns=["Year", "Month", "Total"])
    
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)


    # Drop rows without valid dates
    df = df.dropna(subset=["Date"])
    if df.empty:
        return pd.DataFrame(columns=["Year", "Month", "Total"])
    
    
    # Extract Year & Month names
    df["Year"] = df["Date"].dt.year.astype(int)
    df["Month"] = df["Date"].dt.strftime("%b")

    # Group by Year and Month
    overview_df = (
        df.groupby(["Year", "Month"], as_index=False)["Amount"]
        .sum()
        .rename(columns={"Amount": "Total"})
    )

    
    # Sort chronologically by Year and calender month order
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    overview_df["Month"] = pd.Categorical(overview_df["Month"], categories=month_order, ordered=True)
    overview_df = overview_df.sort_values(["Year", "Month"]).reset_index(drop=True)

    return overview_df



# ----------------------------------------------------------------------------------------------------
# 🧮 PURE FUNCTION (Yearly Totals only)
# ----------------------------------------------------------------------------------------------------
def yearly_total_summary(file_path: str | Path = DATA_FILE) -> pd.DataFrame:
    """
    Summarize total amount spent per year only.

    Args:
        file_path (str | Path): Path to the CSV data file.

    Returns:
        pd.DataFrame: DataFrame with ['Year', 'Total'] columns.
    """
    detailed_df = yearly_overview(file_path)
    if detailed_df.empty:
        return pd.DataFrame(columns=["Year", "Total"])
    
    yearly_df = (
        detailed_df.groupby("Year", as_index=False)["Total"]
        .sum()
        .sort_values("Year")
        .reset_index(drop=True)
    )
    return yearly_df



# ----------------------------------------------------------------------------------------------------
# 💬 CLI DISPLAY WRAPPER
# ----------------------------------------------------------------------------------------------------
def yearly_overview_interactive(file_path: str | Path = DATA_FILE):
    """
    CLI interface for yearly overview display.
    Prints both month-wise and year-wise summaries.
    """
    overview_df = yearly_overview(file_path)
    yearly_df = yearly_total_summary(file_path)

    if overview_df.empty:
        print("⚠️ No expense data available for yearly overview.")
        return

    print("\n📆 Yearly Overview (Month-wise)")
    print(tabulate(overview_df, headers="keys", showindex=False, tablefmt="grid", floatfmt=".2f"))

    if not yearly_df.empty:
        print("\n💰 Yearly Total Summary")
        print(tabulate(yearly_df, headers="keys", showindex=False, tablefmt="grid", floatfmt=".2f"))

        grand_total = yearly_df["Total"].sum()
        print(f"\n🏁 Grand Total Across All Years: ₹{grand_total:.2f}")



# ----------------------------------------------------------------------------------------------------
# 🧪 STANDALONE EXECUTION
# ----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    yearly_overview_interactive()