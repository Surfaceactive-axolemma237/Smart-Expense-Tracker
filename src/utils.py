# src/utils.py
"""
Utility Functions - Smart Expense Tracker
-----------------------------------------
Common helper utilities shared across modules:
    - Date parsing and formatting.
    - Currency formatting.
    - Input validation and conversion.
"""

from datetime import datetime, date
from src.config import DEFAULT_CURRENCY, get_currently_symbol


# ----------------------------------------------------------------------------------------------------
# Date Utilities
# ----------------------------------------------------------------------------------------------------
def parse_date(text: str):
    """
    Parse a text input into a standard ISO date string (YYYY-MM-DD).

    Args:
        text (str): Date input from user or CSV, e.g., "2025-10-12" or "12/10/2025"

    Returns:
        str: ISO date string (YYYY-MM-DD)
             Today's date if blank
             None if unparsable
    """
    if not text or text.strip() == "":
        return date.today().isoformat()
    
    text = text.strip()
    formats = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%b %d, %Y", "%d %b %Y")

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.date().isoformat()
        except ValueError:
            continue

    return None


def format_date(dt):
    """
    Converts a datetime/date object to a user-friendly string (e.g., '12 Oct 2025').
    """
    if isinstance(dt, (datetime, date)):
        return dt.strftime("%d %b %Y")
    return dt



# ----------------------------------------------------------------------------------------------------
# Currency Utilities
# ----------------------------------------------------------------------------------------------------
def format_currency(amount, code="INR"):
    """
    Format a numeric value as currency with proper symbol.

    Args:
        amount (Float|int): Numeric value.
        code (str): Currency code (default: 'INR').

    Returns:
        str: Formatted currency string (e.g., '₹1,250.50')
    """
    try:
        symbol = get_currently_symbol(code)
        return f"{symbol}{float(amount):.2f}"
    except Exception:
        return f"{DEFAULT_CURRENCY}{amount}"
    


# ----------------------------------------------------------------------------------------------------
# Validation Utilities
# ----------------------------------------------------------------------------------------------------
def is_valid_amount(value):
    """
    Validate whether a value can be converted to a positive float.

    Args:
        value (any): User input.

    Returns:
        bool: True if valid positive number, else False.
    """
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False
    


def safe_float(value, default=0.0):
    """
    Safely convert a value to float; returns default on failure.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default