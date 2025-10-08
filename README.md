# 💰 Smart Expense Tracker

A simple yet powerful **Expense Tracking System** built in Python.  
This project helps users **log, view, and analyze** their daily expenses using a local CSV file as a lightweight database.  
Ideal for beginners learning Python as well as for showcasing clean, professional project structure.

---

## 🧠 Features (Phase 1 & 2)

### ✅ Core Features (MVP)
- Add new expenses with **date, category, description, and amount**
- Store data in a local **CSV file**
- View all expenses in a **neatly formatted table**
- Simple **command-line interface (CLI)**
- Basic **error handling** for invalid inputs or missing files

### 🌟 Optional Extras (Future Upgrades)
- Search and filter expenses by category/date
- Summarize monthly totals
- Visualize spending with **charts (matplotlib)**
- Export reports
- Add user authentication (optional advanced feature)

---

## 🧰 Tech Stack
- **Python 3.10+**
- **Libraries:**
  - `pandas` → for data handling
  - `matplotlib` → for visualization
  - `tabulate` → for pretty table display

---

## ⚙️ Setup & Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/<your-username>/smart-expense-tracker.git
   cd smart-expense-tracker
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the program**
   ```bash
   python main.py
   ```

## 📊 Project Flow (Overview)

+---------------------------+
|   User selects an option  |
+-----------+---------------+
            |
            ▼
+---------------------------+
| 1. Add Expense            |
|  - Input data             |
|  - Save to CSV file       |
+---------------------------+
| 2. View Expenses          |
|  - Read CSV file          |
|  - Display in table form  |
+---------------------------+
| 3. Exit                   |
+---------------------------+

## 🧩 Folder Structure

Smart-Expense-Tracker/
│
├── venv/                 # Virtual environment
├── data/                 # Stores CSV files
│   └── expenses.csv
├── main.py               # Main entry point
├── requirements.txt      # Dependencies
├── .gitignore            # Git ignored files
└── README.md             # Project info

## 🧩 Smart Expense Tracker — Feature Definition
### 1. Add Expense
• User can enter:
   • Date (auto-generated or user-input)
   • Category (e.g. Food, Travel, Bills etc.)
   • Description (optional short note)
   • Amount (numeric)
• Data is stored in a CSV file (expenses.csv).

### 2. View Expenses
• Displays all expenses in a neat tabular format.
• Shows columns: Date | Category | Description | Amount
• Handles empty files or missing data gracefully.

### 3. Filter Expenses
• View expenses by:
   • Category
   • Date Range
   • Minimum Amount / Maximum Amount

### 4. CLI Menu System
• Simple numbered Menu:
```pgsql
1. View All Expenses
2. View by Category
3. View by Date Range
4. View by Amount Range
5. Add Expense
6. Exit
```
• Loops until user chooses "Exit".

### 5. Error Handling 
• Prevents crashes on invalid inputs.
• Displays friendly error messages (e.g. "invalid choice, please try again.").
• Automatically creates expenses.csv if not found.

## Optional / Future Features (Post-MVP)
## 1. Edit or Delete Expenses Entries
      • Modify or remove specific entries using an ID or index.
## 2. Summary Reports
      • Show total spending by category or month.
      • Generate pie charts (matplotlib/pandas integration)
## 3. Data Backup / Export
      • Export expenses to Excel or PDF.
      • Automatic daily or weekly backups.
## 4. Budget Limit Alerts
      • Notify user when total 
      • Notify user when total spending exceeds a monthly budget.
## 5. Search Function
      • Find expenses by keyword or description text.
## 6. GUI or Web Interface
      • Upgrade from CLI to a simple GUI (Tkinter/Streamlit)

----------------------------------------------------------------------------------------------------------

## 🔄 Basic Data Flow (Smart Expense Tracker)
### 1️⃣ User Interaction (CLI Menu)
• User runs the program and is shown menu options:
```pgsql
1. View All Expenses
2. View by Category
3. View by Date Range
4. View by Amount Range
5. Add Expense
6. Exit
```
### 2️⃣ Add Expense Flow
• User selects "Add Expense".
• Inputs → Category, Description, Amount (and optionally Date).
• Program validate input.
• Data appended to expenses.csv as:
```bash
date, category, description, amount
2025-10-07, Food, Lunch at Cafe, 250
```

3️⃣ View Expense Flow
• User selects a viewing option.
• Program reads data from expenses.csv.
• Based on user choice:
   • Displays all expenses.
   • Filters by category/date/amount.
• Output displayed in formatted table in terminal.

4️⃣ File Handling
• At startup:
   • Checks if expenses.csv exists.
   • If not, creates it with headers.
• On each "Add Expense":
   • Appends a new line to CSV.
• On "View Expense":
   • Reads data using csv.DictReader().

5️⃣ Error Handling & Exit
• Invalid input → Shows friendly message and loops back.
• “Exit” → Ends program gracefully.

## 🧑‍💻 Author

Varun Wagle
Learner | Builder | Generative AI Enthusiast
💼 [GitHub](https://github.com/Varun-Wagle) | [LinkedIn](https://www.linkedin.com/in/varunwagle/)

----------------------------------------------------------------------------------------------------------

# 🏁 Status

• ✅ Phase 1: Project Setup & Planning – Completed
• ✅ Phase 2: Core Architecture Design – Completed
   - 📂 All code and documentation are in sync and working correctly.
   - 🧱 Ready to move to Phase 3: Feature Enhancement & Analytics.
• 🚀 Phase 3: Feature Enhancement & Analytics