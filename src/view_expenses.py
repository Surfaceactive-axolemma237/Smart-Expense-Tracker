# src/view_expenses.py
"""
Module: view_expenses
---------------------
Handles viewing, filtering, and sorting expense records.

Structure:
    1. get_expenses_df()            → Core Logic (Pure Function)
    2. view_expenses_interactive()  → CLI interface
    3. helper functions             → Sorting/Filtering utilities
"""

import pandas as pd
from tabulate import tabulate
from pathlib import Path
from src.data_manager import ensure_csv_exists, get_data_file


# -------------------------------------------------------------------------------------------------
# 🧠 CORE DATA FUNCTION (Pure / Testable)
# -------------------------------------------------------------------------------------------------
def get_expenses_df(category=None, month=None, sort_by=None, descending=False, file_path=None):
    """
    Load and optionally filter or sort expenses from the CSV.

    Parameters:
        category (str, optional): Filter by category.
        month (str, Optional): Filter by month (format: "YYYY-MM").
        sort_by (str, optional): Column name to sort by ("Amount" or "Date").
        decending (bool): Whether to sort in decending order.
        file_path (Path or str, optional): CSV file to load.

    Return:
        pd.DataFrame: Filtered and/or sorted expense DataFrame.
    """
    ensure_csv_exists()
    file_path = Path(file_path or get_data_file())
    df = pd.read_csv(file_path)

    # ---- Filters ----
    if category:
        df = df[df["Category"].str.lower() == category.lower()]

    if month:
        df = df[df["Date"].astype(str).str.startswith(month)]

    # ---- Sorting ----
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=not descending)

    # ✅ Always return DataFrame (not None)
    return df.reset_index(drop=True)
    

# -------------------------------------------------------------------------------------------------
# 💬 INTERACTIVE VIEW (CLI Layer)
# -------------------------------------------------------------------------------------------------
def view_expenses_interactive():
    """
    CLI Function for viewing, filtering, and sorting expenses.
    """
    ensure_csv_exists()
    df = get_expenses_df()

    if df.empty:
        print("⚠️ No expenses recorded yet.")
        return
    
    while True:
        print("\n=== View Expenses ===")
        print("1. View All")
        print("2. Filter by Category")
        print("3. Filter by Month (YYYY-MM)")
        print("4. Sort by Amount (High → Low)")
        print("5. Sort by Date (Newest → Oldest)")
        print("6. Return to Main Menu")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            filtered_df = df
        elif choice == "2":
            category = input("Enter Category Name: ").strip()
            filtered_df = get_expenses_df(category=category)
        elif choice == "3":
            month = input("Enter Month (YYYY-MM): ").strip()
            filtered_df = get_expenses_df(month=month)
        elif choice == "4":
            filtered_df = get_expenses_df(sort_by="Amount", descending=True)
        elif choice == "5":
            filtered_df = get_expenses_df(sort_by="Date", descending=True)
        elif choice == "6":
            print("Returning to Main Main...")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")
            continue

        # ---- Display Table ----
        if filtered_df.empty:
            print("⚠️ No matching records found.")
            continue

        print("\n" + tabulate(
            filtered_df,
            headers="keys",
            showindex=False,
            tablefmt="grid",
            floatfmt=".2f"
        ))

        total = filtered_df["Amount"].sum()
        print(f"\n💰 Total in selection: ₹{total:.2f}")

        again = input("\nView again (Y/N): ").strip().lower()
        if again != "y":
            break


# -------------------------------------------------------------------------------------------------
# 🧪 STANDALONE RUNNER
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    view_expenses_interactive()