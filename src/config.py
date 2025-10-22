# src/config.py
"""
Configuration Module - Smart Expense Tracker
--------------------------------------------
Centralized configuration for global constants, file paths,
currency preferences, and stylistic settings.

Future exxpansions:
------------------
    - User preferences (theme, chart color, etc.)
    - Multi-Language or localization support.
    - Environment variables integration for production.
"""

from pathlib import Path


# ----------------------------------------------------------------------------------------------------
# Project and Data File Configuration
# ----------------------------------------------------------------------------------------------------
# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent


# Define the data directory and default expense file
DATA_DIR = ROOT_DIR / "data"
DATA_FILE = DATA_DIR / "Expenses.csv"
LOGS_DIR = ROOT_DIR / "logs"
VISUALS_DIR = ROOT_DIR / "Visuals"

# Ensure directories exist
for folder in [DATA_DIR, LOGS_DIR, VISUALS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------------------------------
# Currency Configuration
# ----------------------------------------------------------------------------------------------------
# Default currency symbol - India (INR)
DEFAULT_CURRENCY = "₹"

# Supported currencies (easily expandable)
SUPPORTED_CURRENCIES = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "CNY": "¥",
    "SAR": "﷼",
}


# ----------------------------------------------------------------------------------------------------
# Application Constants
# ----------------------------------------------------------------------------------------------------
APP_NAME = "Smart Expense Tracker"
VERSION = "3.0"
AUTHOR = "Varun Wagle"


# Visualization Defaults
COLOR_PALETTE = "crest" # Seaborn-Compatible palette


# ----------------------------------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------------------------------
def get_currently_symbol(code: str) -> str:
    """
    Retrieve the currency symbol for a given currency code.

    Args:
        code (str): Currency code (e.g., 'INR', 'USD').

    Returns:
        str: Corresponding symbol, defaults to INR if not found.
    """
    return SUPPORTED_CURRENCIES.get(code.upper(), DEFAULT_CURRENCY)


# ----------------------------------------------------------------------------------------------------
# Test Mode Configuration
# ----------------------------------------------------------------------------------------------------
TEST_MODE = False
TEST_VISUALS_DIR = LOGS_DIR / "Visuals"
TEST_VISUALS_DIR.mkdir(parents=True, exist_ok=True)