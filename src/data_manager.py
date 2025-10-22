# src/data_manager.py
"""
Module: data_manager
Manages loading, saving, and validating the expense data CSV file.

This module ensures:
    - A consistent data directory and file path.
    - Automatic CSV creation with correct headers.
    - Safe loading/saving operations for both CLI and GUI use.
"""

import csv
import pandas as pd
from pathlib import Path
from src.config import DATA_FILE


# -------------------- Global Constants --------------------
DEFAULT_HEADERS = ["Date", "Category", "Description", "Amount", "Payment_Mode"]


# -------------------- File Handling --------------------
def get_data_file() -> Path:
    """
    Get or create the main expense CSV file path.

    Return:
        Path: Absolute path to the expense data file.
    """
    file_path = Path(DATA_FILE)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def ensure_csv_exists(file_path: Path | None = None) -> None:
    """
    Ensure the data CSV exists and has the proper headers.
    If not, it will be created automatically.

    Args:
        file_path (Path | None): Optional custom CSV path.
    """
    file_path = Path(file_path or get_data_file())

    if not file_path.exists() or file_path.stat().st_size == 0:
        with file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(DEFAULT_HEADERS)
        print(f"✅ Created new data file: {file_path}")


# -------------------- Data Loading --------------------
def load_expenses(file_path: Path | None = None) -> pd.DataFrame:
    """
    Load expense data into a DataFrame with validated columns and types.

    Args:
        file_path (Path | None): Optional custom CSV path.

    Returns:
        pd.DataFrame: Expense DataFrame (empty if not found or invalid).
    """
    file_path = Path(file_path or get_data_file())
    ensure_csv_exists(file_path)

    try:
        df = pd.read_csv(file_path)


        # Ensure all expected columns exist
        for col in DEFAULT_HEADERS:
            if col not in df.columns:
                df[col] = None

        
        # Test Casting
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)


        # Drop invalid rows (no data or amount)
        df = df.dropna(subset=["Date"])
        return df[DEFAULT_HEADERS]
    
    except Exception as e:
        print(f"⚠️ Error loading expenses: {e}")
        return pd.DataFrame(columns=DEFAULT_HEADERS)
    

# -------------------- Data Saving --------------------
def save_expenses(df: pd.DataFrame, file_path: Path | None = None) -> None:
    """
    Save expenses DataFrame safely to CSV.

    Args:
        df (pd.DataFrame): Data to save.
        file_path (Path | None): Optional custom path.
    """
    file_path = Path(file_path or get_data_file())
    ensure_csv_exists(file_path)

    try:
        df.to_csv(file_path, index=False, encoding="utf-8")
    except Exception as e:
        print(f"⚠️ Error saving expenses: {e}")


# -------------------- Data Appending --------------------
def append_expense(entry: dict, file_path: Path | None = None) -> None:
    """
    Append a new single expense record to the CSV file.

    Args:
        entry (dict): A dictionary containing the expense record.
        file_path (Path | None): Optional custom CSV path.
    """
    file_path = Path(file_path or get_data_file())
    ensure_csv_exists(file_path)

    try:
        df = load_expenses(file_path)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        save_expenses(df, file_path)
    except Exception as e:
        print(f"⚠️ Error appending new expenses: {e}")


# -------------------- CLI Diagnostic --------------------
if __name__ == "__main__":
    ensure_csv_exists()
    df = load_expenses()
    if df.empty:
        print("📂 No expense records yet.")
    else:
        print(f"📊 Loaded {len(df)} expense entries.")
        print(df.head())