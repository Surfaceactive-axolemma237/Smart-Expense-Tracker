# src/main.py
"""
Smart Expense Tracker — Add expense (beginner-friendly)
Place this file at: Smart-Expense-Tracker/src/main.py
Run: python src/main.py
"""

from tabulate import tabulate
import csv
import os
from pathlib import Path
from datetime import datetime, date

# ---------- Project paths & CSV discovery ----------
ROOT = Path(__file__).resolve().parent.parent

def get_data_file():
    """
    Locate an existing CSV if present (supporting different capitalizations users may have used),
    otherwise create a standard path: <ROOT>/data/expenses.csv
    """
    candidates = [
        ROOT / "Data" / "Expenses.csv",
        ROOT / "data" / "expenses.csv",
        ROOT / "Data" / "expenses.csv",
        ROOT / "data" / "Expenses.csv",
    ]
    for p in candidates:
        if p.exists():
            return p

    # default to lowercase 'data/expenses.csv' if nothing found
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "expenses.csv"

CSV_FILE = get_data_file()


# ---------- Ensure CSV exists with headers ----------
def ensure_csv_exists():
    """
    Make sure the CSV file is present and has header row.
    This is safe to run every time the program starts.
    """
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Description", "Amount", "Payment_Mode"])
        print(f"✅ Created new data file: {CSV_FILE}")
    else:
        # file exists and likely has data
        pass


# ---------- Small helper to parse dates ----------
def parse_date(text: str):
    """
    Accepts common date formats and returns ISO date string (YYYY-MM-DD).
    If text is empty/None -> returns today's date.
    If not parseable -> returns None.
    """
    if not text or text.strip() == "":
        return date.today().isoformat()
    text = text.strip()
    formats = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")
    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.date().isoformat()
        except ValueError:
            continue
    return None


# ---------- Core feature: add_expense ----------
def add_expense():
    """
    Interactively ask user for expense details, validate them,
    and append as a new row to the CSV file.
    Type 'q' at any prompt to cancel.
    """
    print("\n=== Add a new expense (type 'q' to cancel at any prompt) ===")

    # 1) Date (optional; default = today)
    while True:
        user_date = input("Date (YYYY-MM-DD) [press Enter for today]: ").strip()
        if user_date.lower() == "q":
            print("Canceled.")
            return
        parsed = parse_date(user_date)
        if parsed is not None:
            date_value = parsed
            break
        else:
            print("Invalid date format. Try YYYY-MM-DD or DD/MM/YYYY. (or press Enter for today)")

    # 2) Category (required)
    while True:
        category = input("Category (e.g., Food, Travel, Bills): ").strip()
        if category.lower() == "q":
            print("Canceled.")
            return
        if category == "":
            print("Category cannot be empty. Please enter one.")
        else:
            break

    # 3) Description (optional)
    description = input("Description (optional): ").strip()
    if description.lower() == "q":
        print("Canceled.")
        return

    # 4) Amount (required; numeric)
    while True:
        amount_str = input("Amount (e.g., 12.50): ").strip()
        if amount_str.lower() == "q":
            print("Canceled.")
            return
        try:
            amount = float(amount_str)
            if amount < 0:
                print("Amount cannot be negative. Enter a positive number.")
                continue
            amount = round(amount, 2)  # keep two decimals
            break
        except ValueError:
            print("Invalid amount. Please enter a number like 12.50 or 100.")

    # 5) Payment mode (optional)
    payment_mode = input("Payment mode (Cash/UPI/Card) [optional]: ").strip()
    if payment_mode.lower() == "q":
        print("Canceled.")
        return

    # ---------- Append to CSV safely ----------
    try:
        write_header = not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0
        with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
            fieldnames = ["Date", "Category", "Description", "Amount", "Payment_Mode"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow({
                "Date": date_value,
                "Category": category,
                "Description": description,
                "Amount": f"{amount:.2f}",
                "Payment_Mode": payment_mode
            })
        print(f"✅ Expense added: {date_value} | {category} | {description} | {amount:.2f} | {payment_mode}")
    except Exception as e:
        print("❌ Failed to save expense. Error:", e)

# ---------- Minimal test menu (so you can run & try view_expense) ----------
def view_expenses():
    file_path = CSV_FILE

    if not os.path.exists(file_path):
        print("No expenses found yet. Add some first.")
        return
    
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if not data:
        print("No expenses recorded yet.")
        return
    
    # ----------- Filter option -----------
    print("\nFilter Option:")
    print("1. View All Expenses")
    print("2. Filter by Date Range")
    print("3. Filter by Category")
    print("4. Filter by Both Date Range & Category")

    choice = input("\nEnter your choice (1-4): ").strip()

    filtered_data = data # Default

    if choice == "1":
        print("\nShowing all expenses...\n")

    if choice == "2" or choice == "4":
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            filtered_data = [
                row for row in filtered_data
                if start_date <= datetime.strptime(row["Date"], "%Y-%m-%d") <= end_date
            ]
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    if choice == "3" or choice == "4":
        category = input("Enter category name (case-insensitive): ").strip().lower()
        filtered_data = [
            row for row in filtered_data
            if row["Category"].lower() == category
        ]

    # ----------- Display Results -----------
    if filtered_data:
        print("\nFiltered Expenses:\n")
        print(tabulate(
            [[r["Date"], r["Category"], r["Description"], r["Amount"], r["Payment_Mode"]] for r in filtered_data], 
            headers=["Date", "Category", "Description", "Amount", "Payment_Mode"],
            tablefmt="fancy_grid"
        ))
        print(f"\nTotal Records: {len(filtered_data)}")
    else:
        print("\nNo matching records found for the given filters.")

# ---------- Minimal test menu (so you can run & try add_expense) ----------
def main():
    ensure_csv_exists()
    while True:
        print("\nSmart Expense Tracker — Menu")
        print("1) Add Expense")
        print("2) View Expenses")
        print("3) Exit")
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3" or choice.lower() == "q":
            print("Goodbye — your data is stored in:", CSV_FILE)
            break
        else:
            print("Invalid option. Enter 1-3.")

if __name__ == "__main__":
    main()
