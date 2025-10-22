# src/main.py
"""
Smart Expense Tracker - Central Control Hub
-------------------------------------------
Phase 6 - Unified Integration

This script serves as the main entry point of the Smart Expense Tracker.
It integrates all modules, provides a menu-driven interface,
and manages start-up diagnostics and data readiness.

Modules Integrated:
    • add_expense.py
    • view_expenses.py
    • monthly_summary.py
    • category_insight.py
    • yearly_overview.py
    • visualization.py
    • config.py
"""


import sys
import os
from pathlib import Path

# ----- Ensure project root is in import path -----
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Imports for test diagnostics
try:
    from tests.test_integration import run_all_tests
except ImportError:
    run_all_tests = lambda: print("⚠️ Skipping diagnostics: test suite not found.")

# Core Configuration
from src.config import (
    APP_NAME,
    VERSION,
    AUTHOR,
    DATA_FILE,
    DEFAULT_CURRENCY,
    get_currently_symbol,
)

# Functional modules
from src import (
    add_expense,
    view_expenses,
    monthly_summary,
    category_insight,
    yearly_overview,
    visualization,
)
from src.data_manager import load_expenses


# ----------------------------------------------------------------------------------------------------
# Start-Up Diagnostics
# ----------------------------------------------------------------------------------------------------
def bios_self_check():
    from src import config
    """Run integrated test diagnostics."""
    print("\n🩺 Running system diagnostics...")
    try:
        config.TEST_MODE = True
        run_all_tests()
        config.TEST_MODE = False
    except Exception as e:
        print(f"⚠️ Diagnostics skipped or failed: {e}")
    print("✅ Diagnostics Complete.\n")



# ----------------------------------------------------------------------------------------------------
# Ensure CSV Exists
# ----------------------------------------------------------------------------------------------------
def ensure_csv_exists():
    """Ensure that the expense CSV file exists with proper headers."""
    data_path = Path(DATA_FILE)
    if not data_path.exists():
        print(f"⚙️ Creating data file at: {DATA_FILE}")
        data_path.parent.mkdir(parents=True, exist_ok=True)
        import pandas as pd

        df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Currency"])
        df.to_csv(DATA_FILE, index=False)



# ----------------------------------------------------------------------------------------------------
# Header Display
# ----------------------------------------------------------------------------------------------------
def show_header():
    """Display application metadata."""
    print("\n" + "=" * 60)
    print(f"{APP_NAME} v{VERSION}")
    print(f"Author: {AUTHOR}")
    print("=" * 60)


# # ----------------------------------------------------------------------------------------------------
# # Visualization Menu
# # ----------------------------------------------------------------------------------------------------
from src.visualization import visualization_interactive


# ----------------------------------------------------------------------------------------------------
# Testing & Debugging Menu
# ----------------------------------------------------------------------------------------------------
def run_testing_debugging():
    """Run self-tests and data integrity checks."""
    print("\n🧩 Testing & Debugging Mode")
    print("-" * 50)
    print(f"Data File: {DATA_FILE}")
    print(f"Exists: {Path(DATA_FILE).exists()}")
    print(f"Default Currency: {DEFAULT_CURRENCY} ({get_currently_symbol(DEFAULT_CURRENCY)})")

    df = load_expenses(DATA_FILE)
    print(f"Rows in dataset: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    if not df.empty:
        print("\n📘 Sample Data Preview:")
        print(df.head(5).to_string(index=False))
    else:
        print("\n⚠️ Dataset is empty. Add some exxpenses first.")

    input("\nPress Enter to return to the Main Menu...")



# ----------------------------------------------------------------------------------------------------
# Main Menu
# ----------------------------------------------------------------------------------------------------
def main_menu():
    """Main Interactive Menu."""
    while True:
        show_header()
        print("\nSelect an option:")
        print("1. ➕ Add New Expense")
        print("2. 📋 View / Filter Expenses")
        print("3. 📅 Monthly Summary")
        print("4. 🏷️ Category Insights")
        print("5. 📆 Yearly Overview")
        print("6. 📈 Visualization Dashboard")
        print("7. 🧠 Testing & Debugging")
        print("8. 🚪 Exit")

        choice = input("\nEnter your Choice (1-8): ").strip()

        if choice == "1":
            add_expense.add_expense_interactive()
        elif choice == "2":
            view_expenses.view_expenses_interactive()
        elif choice == "3":
            monthly_summary.monthly_summary_interactive()
        elif choice == "4":
            category_insight.category_insight_interactive()
        elif choice == "5":
            yearly_overview.yearly_overview_interactive()
        elif choice == "6":
            visualization_interactive()
        elif choice == "7":
            run_testing_debugging()
        elif choice == "8":
            print("\nThank you for using Smart Expense Tracker! 👋")
            break
        else:
            print("⚠️ Invalid choice, please try again.\n")


# ----------------------------------------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    bios_self_check()
    ensure_csv_exists()
    main_menu()