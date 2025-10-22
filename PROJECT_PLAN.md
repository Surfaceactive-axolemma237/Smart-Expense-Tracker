# 🧭 Smart Expense Tracker — Project Plan

A modular, test-driven, and analytics-enabled CLI application for personal expense management.

---

## ✅ Phase 1 — Core Expense Management
📂 **Goal:** Build the basic expense tracking system (data + logic)

**Status:** ✔️ *Completed*

**Modules:**
- [x] `add_expense.py` — Add new expense entries  
- [x] `view_expenses.py` — View, filter, and sort expenses  
- [x] `data_manager.py` — File I/O handling and CSV schema  
- [x] `utils.py` — Helper utilities (date parsing, validation)

**Deliverables:**
- [x] Functional CLI options (Add, View)
- [x] Persistent CSV file: `data/Expenses.csv`
- [x] Input validation and error handling

---

## ✅ Phase 2 — Modularization + Testing Foundation
📂 **Goal:** Refactor into modular testable structure using Pytest

**Status:** ✔️ *Completed*

**Updates:**
- [x] Split logic & interactive layers  
- [x] Added `/src` and `/tests` structure  
- [x] Introduced Pytest-based self-testing system  
- [x] Implemented `bios_self_check()` inside `main.py`

**Deliverables:**
- [x] Each function independently testable  
- [x] CLI layer separated from backend logic  
- [x] Self-check executes all tests automatically

---

## ✅ Phase 3 — Visualization & Analytics
📊 **Goal:** Add financial insights and visual dashboards

**Status:** ✔️ *Completed*

**Analytics Modules:**
- [x] `monthly_summary.py` — Monthly aggregation  
- [x] `category_insight.py` — Spending by category  
- [x] `yearly_overview.py` — Yearly + month-wise summaries  

**Visualization:**
- [x] `visualization.py` with 7 chart types  
- [x] CLI Visualization Dashboard  
- [x] Smart y-limit rounding & label overlap prevention  
- [x] Charts auto-saved in `/Visuals/` (CLI) and `/logs/Visuals/` (Tests)
- [x] Color-coded CLI outputs (🟢 Normal | 🟡 Test Mode)

---

## ⚙️ Phase 4 — Integration & Finalization
**Goal:** Integrate all modules and prepare release

**Status:** ✔️ *Completed*

**Tasks:**
- [x] `main.py` integrated with all modules  
- [x] `config.py` centralized settings  
- [x] Logging system: `/logs/test_reports/` + `/logs/Visuals/<timestamp>/`  
- [x] Full self-test automation  
- [x] Clean CLI with consistent design & headers  

---

## 🧠 Phase 5 — Future Enhancements (v2.5+)
**Goal:** Expand usability and intelligence  

**Status:** ⏳ *Planned*

**Ideas:**
- [ ] GUI using Tkinter / Streamlit / PyQt  
- [ ] Export charts to PDF reports  
- [ ] Multi-user profiles & multi-currency support  
- [ ] AI-based budget analysis  
- [ ] Cloud sync / SQLite database backend  

---

### 🗂 Directory Structure

Smart-Expense-Tracker/
│
├── src/
│ ├── add_expense.py
│ ├── view_expenses.py
│ ├── monthly_summary.py
│ ├── category_insight.py
│ ├── yearly_overview.py
│ ├── visualization.py
│ ├── data_manager.py
│ ├── utils.py
│ └── config.py
│
├── data/
│ └── Expenses.csv
│
├── logs/
│ ├── test_reports/
│ └── Visuals/<timestamp>/
│
├── tests/
│ ├── test_add_expense.py
│ ├── test_view_expenses.py
│ ├── test_monthly_summary.py
│ ├── test_category_insight.py
│ ├── test_yearly_overview.py
│ └── test_visualization.py
│
├── Visuals/
│── README.md
└── PROJECT_PLAN.md


---

### 🏁 Project Metadata
- **App Name:** Smart Expense Tracker  
- **Version:** 2.0  
- **Author:** Varun Wagle  
- **License:** MIT (planned)  
- **Frameworks:** Python 3.13, Pandas, Matplotlib, Seaborn, Pytest  


