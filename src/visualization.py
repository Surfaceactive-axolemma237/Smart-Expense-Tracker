# src/visualization.py
"""
Visualization Module - Smart Expense Tracker
--------------------------------------------
Generates visual insights using Matplotlib and Seaborn.

Features:
    - All charts saved automatically to /Visuals/
    - In test mode: saved under /logs/Visuals/<timestamp>/
    - Safe label placement (no overlap) and readable black text
"""

import os, math, datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from matplotlib.transforms import Bbox
from src.data_manager import load_expenses
from src.config import (
    DATA_FILE, COLOR_PALETTE, DEFAULT_CURRENCY,
    TEST_MODE, TEST_VISUALS_DIR, VISUALS_DIR,
    APP_NAME, VERSION, AUTHOR
)

# --- Fix import path for standalone execution ---
if __package__ is None or __package__ == "":
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_manager import load_expenses
from src.config import DATA_FILE, COLOR_PALETTE, DEFAULT_CURRENCY

sns.set(style="whitegrid")

# Directory to store generated charts
VISUALS_DIR = Path(__file__).resolve().parent.parent / "Visuals"
VISUALS_DIR.mkdir(parents=True, exist_ok=True)

# Core Configuration
from src.config import (
    APP_NAME,
    VERSION,
    AUTHOR,
    DATA_FILE,
    DEFAULT_CURRENCY,
    get_currently_symbol,
)


# ----------------------------------------------------------------------------------------------------
# 🧩 Internal Helper: Fetch and Clean Data
# ----------------------------------------------------------------------------------------------------
def _get_data(file_path: str | Path = DATA_FILE) -> pd.DataFrame:
    """Fetch and clean expense data for visualization."""
    file_path = str(file_path or DATA_FILE)
    try:
        df = load_expenses(file_path)
    except Exception:
        if Path(file_path).exists():
            df = pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

    if df.empty:
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df = df.dropna(subset=["Date", "Category"], how="any")
    if df.empty:
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


# ----------------------------------------------------------------------------------------------------
# 💾 Utility: Save Chart
# ----------------------------------------------------------------------------------------------------
def _save_chart(fig, chart_name: str):
    """
    Save charts in either /Visuals/ or /logs/Visuals/<timestamp>/ depending on TEST_MODE.
    Dynamically checks config.TEST_MODE every call to stay in sync with test environment.
    """
    from src import config  # dynamic import ensures latest TEST_MODE value

    # Re-fetch live flag in case it was toggled after import
    test_mode = getattr(config, "TEST_MODE", False)
    test_dir = getattr(config, "TEST_VISUALS_DIR", Path("logs/Visuals"))

    # Select folder based on mode
    if test_mode:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = test_dir / timestamp
        folder.mkdir(parents=True, exist_ok=True)
        prefix = "\033[93m🟡 [Test Mode]\033[0m"  # Yellow text
    else:
        folder = VISUALS_DIR
        folder.mkdir(parents=True, exist_ok=True)
        prefix = "\033[92m🟢\033[0m"  # Green text

    # Sanitize filename and save
    filename = f"{chart_name.replace(' ', '_')}.png"
    save_path = folder / filename
    fig.savefig(save_path, bbox_inches="tight")
    print(f"{prefix} Chart saved → {save_path}")
    plt.close(fig)


# ----------------------------------------------------------------------------------------------------
# 1️⃣ Monthly Spending Overview
# ----------------------------------------------------------------------------------------------------
def plot_monthly_spending(file_path: str | Path = DATA_FILE, show: bool = False):
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    monthly = df.groupby("Month", as_index=False)["Amount"].sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=monthly, x="Month", y="Amount", hue="Month",
                palette=COLOR_PALETTE, legend=False, ax=ax)
    ax.set_title("Monthly Spending Overview")
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Total Spent ({DEFAULT_CURRENCY})")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Monthly Spending Overview")
    return fig


# ----------------------------------------------------------------------------------------------------
# 2️⃣ Monthly Spending by Category
# ----------------------------------------------------------------------------------------------------
def plot_monthly_spending_by_category(file_path: str | Path = DATA_FILE, show: bool = False):
    """
    Plot grouped (side-by-side) bars for each month by category
    enclosed within a faint translucent total box.
    """
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    # --- Aggregate data ---
    pivot_df = df.pivot_table(index="Month", columns="Category", values="Amount", aggfunc="sum", fill_value=0)
    monthly_totals = pivot_df.sum(axis=1)
    months = pivot_df.index
    categories = list(pivot_df.columns)
    num_categories = len(categories)

    # --- Setup ---
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("Set2", num_categories)

    # --- Compute bar positions ---
    x = range(len(months))
    bar_width = 0.12
    offsets = [(i - (num_categories - 1) / 2) * bar_width for i in range(num_categories)]

    # --- Smart y-axis bound ---
    highest_total = monthly_totals.max()
    round_base = 10000 if highest_total > 10000 else 1000
    y_max = math.ceil(highest_total / round_base) * round_base
    ax.set_ylim(0, y_max * 1.1)

    # --- Translucent total boxes ---
    for i, total in enumerate(monthly_totals):
        ax.bar(i, total, width=bar_width * (num_categories + 0.4),
               color="lightgray", alpha=0.25,
               edgecolor="gray", linewidth=2, linestyle="--",
               label="_nolegend_" if i > 0 else "Total Spending", zorder=1)

    # --- Bounding-box aware label placement ---
    label_bboxes = []

    def place_label(x, y, text):
        """Place labels safely using bbox collision detection."""
        text_obj = ax.text(x, y, text, ha="center", va="bottom", fontsize=8.5, color="black", zorder=5, clip_on=True)
        fig.canvas.draw()
        bbox_new = text_obj.get_window_extent(renderer=fig.canvas.get_renderer()).transformed(ax.transData.inverted())
        for prev_bbox in label_bboxes:
            if bbox_new.overlaps(prev_bbox):
                text_obj.remove()
                return place_label(x, y + (y_max * 0.03), text)
        label_bboxes.append(bbox_new)
        return text_obj

    # --- Category bars and labels ---
    for idx, cat in enumerate(categories):
        bars = ax.bar([pos + offsets[idx] for pos in x], pivot_df[cat], width=bar_width,
                      color=colors[idx], label=cat, edgecolor="white", zorder=3)
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                x_pos = bar.get_x() + bar.get_width() / 2
                place_label(x_pos, height + (y_max * 0.01), f"₹{int(height)}")

    # --- Total labels ---
    for i, total in enumerate(monthly_totals):
        place_label(i, total + (y_max * 0.03), f"₹{int(total):,}")

    # --- Aesthetics ---
    ax.set_title("Monthly Spending by Category (Side-by-Side with Total Outline)")
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Total Spent ({DEFAULT_CURRENCY})")
    ax.set_xticks(list(x))
    ax.set_xticklabels(months, rotation=45)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Category")
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Monthly_Spending_by_Category")
    return fig


# ----------------------------------------------------------------------------------------------------
# 3️⃣ Spending Trend (Line Chart)
# ----------------------------------------------------------------------------------------------------
def plot_spending_trend(file_path: str | Path = DATA_FILE, show: bool = False):
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    monthly = df.groupby("Month", as_index=False)["Amount"].sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=monthly, x="Month", y="Amount", marker="o", color="teal", ax=ax)
    ax.set_title("Spending Trend Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Total Spent ({DEFAULT_CURRENCY})")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Spending Trend Over Time")
    return fig


# ----------------------------------------------------------------------------------------------------
# 4️⃣ Category Breakdown (Pie)
# ----------------------------------------------------------------------------------------------------
def plot_category_breakdown(file_path: str | Path = DATA_FILE, show: bool = False):
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    category_totals = df.groupby("Category", as_index=False)["Amount"].sum()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(category_totals["Amount"], labels=category_totals["Category"],
           autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
    ax.set_title("Spending by Category")
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Category Breakdown")
    return fig


# ----------------------------------------------------------------------------------------------------
# 5️⃣ Category Heatmap
# ----------------------------------------------------------------------------------------------------
def plot_category_heatmap(file_path: str | Path = DATA_FILE, show: bool = False):
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    pivot_df = df.pivot_table(index="Category", columns="Month",
                              values="Amount", aggfunc="sum", fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Category Spending Heatmap")
    ax.set_xlabel("Month")
    ax.set_ylabel("Category")
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Category Heatmap")
    return fig


# ----------------------------------------------------------------------------------------------------
# 6️⃣ Daily Spending Distribution
# ----------------------------------------------------------------------------------------------------
def plot_daily_distribution(file_path: str | Path = DATA_FILE, show: bool = False):
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["Amount"], bins=20, color="coral", edgecolor="black", alpha=0.8)
    ax.set_title("Daily Spending Distribution")
    ax.set_xlabel(f"Spending Amount ({DEFAULT_CURRENCY})")
    ax.set_ylabel("Frequency")
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Daily Spending Distribution")
    return fig


# ----------------------------------------------------------------------------------------------------
# 7️⃣ Top 5 Expense Items
# ----------------------------------------------------------------------------------------------------
def plot_top_expense_items(file_path: str | Path = DATA_FILE, show: bool = False):
    plt.close("all")
    df = _get_data(file_path)
    if df.empty:
        return None

    top5 = df.nlargest(5, "Amount")[["Date", "Category", "Description", "Amount"]]
    print("\n💰 Top 5 Expense Items:")
    print(top5.to_string(index=False))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top5, x="Description", y="Amount", hue="Category",
                palette="coolwarm", ax=ax)
    ax.set_title("Top 5 Expense Items")
    ax.set_xlabel("Description")
    ax.set_ylabel(f"Amount ({DEFAULT_CURRENCY})")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    if show:
        plt.show()
    _save_chart(fig, "Top 5 Expense Items")
    return fig


# ----------------------------------------------------------------------------------------------------
# Header Display
# ----------------------------------------------------------------------------------------------------
def show_header():
    """Display application metadata."""
    print("\n" + "=" * 60)
    print(f"{APP_NAME} v{VERSION}")
    print(f"Author: {AUTHOR}")
    print("=" * 60)


# ----------------------------------------------------------------------------------------------------
# 💬 CLI Visualization Menu
# ----------------------------------------------------------------------------------------------------
def visualization_interactive(file_path: str | Path = DATA_FILE):
    options = {
        "1": ("📊 Monthly Spending Overview", plot_monthly_spending),
        "2": ("🧩 Monthly Spending by Category", plot_monthly_spending_by_category),
        "3": ("🥧 Category Breakdown (Pie)", plot_category_breakdown),
        "4": ("📈 Spending Trend Over Time", plot_spending_trend),
        "5": ("🔥 Category Heatmap", plot_category_heatmap),
        "6": ("📅 Daily Spending Distribution", plot_daily_distribution),
        "7": ("💰 Top 5 Expense Items", plot_top_expense_items),
    }

    print(f"\n=== Visualization Dashboard ({APP_NAME} v{VERSION}) ===")
    while True:
        for k, (label, _) in options.items():
            print(f"{k}. {label}")
        print("8. 🔙 Return to Main Menu")

        choice = input("\nSelect a chart (1–8): ").strip()

        if choice == "1":
            plot_monthly_spending()
        elif choice == "2":
            plot_monthly_spending_by_category()
        elif choice == "3":
            plot_category_breakdown()
        elif choice == "4":
            plot_spending_trend()
        elif choice == "5":
            plot_category_heatmap()
        elif choice == "6":
            plot_daily_distribution()
        elif choice == "7":
            plot_top_expense_items()
        elif choice == "8":
            print("Returning to Main Menu...")
            break

        entry = options.get(choice)
        if not entry:
            print("⚠️ Invalid selection. Try again.")
            continue

        label, func = entry
        print(f"\nGenerating: {label} ...")
        fig = func(file_path=file_path, show=False)

        if fig is None:
            print("⚠️ No data available for this chart.")
        else:
            print("✅ Chart generated and saved successfully!\n")

        again = input("Would you like to view another chart? (Y/N): ").strip().lower()
        if again != "y":
            break


# ----------------------------------------------------------------------------------------------------
# 🧪 Standalone Run
# ----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    visualization_interactive()
