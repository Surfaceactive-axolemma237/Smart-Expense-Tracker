#src/add_expense.py
"""
Module: add_expense.py
----------------------
Handles adding a new expense entry to the system.

Structure:
    1. add_expense_entry() → Pure, testable function (no user input).
    2. add_expense_interactive() → CLI wrapper for interactive use.

Future-ready: This design will also work for GUI or API layers.
"""

import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
from src.data_manager import ensure_csv_exists,get_data_file
from src.utils import parse_date


# -------------------------------------------------------------------------------------------------
# 🧠 PURE FUNCTION (Used in unit tests and backend operations)
# -------------------------------------------------------------------------------------------------
def add_expense_entry(date, category, description, amount, payment_mode="Cash", file_path=None):
    """
    Add a new expense record to the CSV File.

    Parameters:
        date (str or datetime): Date of the expense.
        category (str): Expense category.
        description (str): Short description.
        amount (float): Expense amount (must be > 0).
        payment_mode (str): Payment method ("Cash", "Card", "UPI", etc.).
        file_path (Path or str, optional): Custom CSV file path for testing.

    Returns:
        dict: The expense entry added.
    """
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    
    ensure_csv_exists()
    file_path = Path(file_path or get_data_file())

    # Convert Date
    if isinstance(date, datetime):
        date_str = date.strftime("%Y-%m-%d")
    else:
        date_str = str(date)

    entry = {
        "Date": date_str,
        "Category": category.strip() or "Uncategorized",
        "Description": description.strip(),
        "Amount": float(amount),
        "Payment Mode": payment_mode.strip() or "Cash"
    }

    # Append new entry to CSV
    df = pd.read_csv(file_path)
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(file_path, index=False)

    return entry


# -------------------------------------------------------------------------------------------------
# Backward-Compatible Wrapper (For self testing)
# -------------------------------------------------------------------------------------------------
def add_expense(date, category, description, amount, payment_mode="Cash", file_path=None):
    """
    Backward-compatible wrapper for add_expense_entry().
    Allows tests and main app to call add_expense() directly.
    """
    return add_expense_entry(date, category, description, amount, payment_mode, file_path)


# -------------------------------------------------------------------------------------------------
# 💬 INTERACTIVE WRAPPER (Used in CLI - main.py)
# -------------------------------------------------------------------------------------------------
def add_expense_interactive():
    """
    CLI-based interactive function for adding an expense.
    Guides user step-by-step through input fields.
    """
    try:
        ensure_csv_exists()

        # ----- Date -----
        date_input = input("Enter Date (YYYY-MM-DD or DD/MM/YYYY) [Leave blank for today]: ").strip()
        date_str = parse_date(date_input)
        if not date_str:
            print("⚠️ Invalid date format. Expense not added.")
            return
        
        # --- Category ---
        category = input("Enter category (e.g., Food, Travel, Bills, Others): ").strip() or "Uncategorized"

        # --- Description ---
        description = input("Enter a short description (Optional): ").strip()

        # ---- Amount ----
        try:
            amount = float(input("Enter amount (₹): ").strip())
            if amount <= 0:
                print("⚠️ Amount must be greater than 0.")
                return
        except ValueError:
            print("⚠️ Invalid amount. Please enter a numeric value.")
            return
        
        # ---- Payment Mode ----
        payment_mode = input("Enter payment mode (Cash/Card/UPI): ").strip() or "Cash"

        # ---- Save Entry ----
        entry = add_expense_entry(date_str, category, description, amount, payment_mode)
        print(f"✅ Expense added successfully on {entry['Date']} ({entry['Category']}: ₹{entry['Amount']:.2f})")

    except KeyboardInterrupt:
        print("\n❌ Operation cancellled by user.")
    except Exception as e:
        print(f"❌ Error adding expense: {e}")

# -------------------------------------------------------------------------------------------------
# 🧪 Standalone Testing
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    add_expense_interactive()