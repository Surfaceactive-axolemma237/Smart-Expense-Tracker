import pytest
import pandas as pd
import tempfile
from pathlib import Path

@pytest.fixture
def sample_csv_file():
    """Create a temporary sample CSV file for testing."""
    # Sample data
    data = [
        ["2025-10-01", "Food", "Lunch", 250],
        ["2025-10-02", "Transport", "Bus", 40],
        ["2025-10-03", "Shopping", "T-Shirt", 1200],
        ["2025-10-04", "Bills", "Electricity", 900],
        ["2025-10-05", "Food", "Dinner", 300]
    ]
    columns = ["Date", "Category", "Description", "Amount"]

    # Create Temporary File
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="") as tmp:
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(tmp.name, index=False)
        tmp_path = Path(tmp.name)

    yield tmp_path

    # Clean after path
    if tmp_path.exists():
        tmp_path.unlink()