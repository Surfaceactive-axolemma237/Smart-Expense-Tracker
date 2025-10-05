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

## 🧑‍💻 Author

Varun Wagle
Learner | Builder | Generative AI Enthusiast
💼 [GitHub](https://github.com/Varun-Wagle) | [LinkedIn](https://www.linkedin.com/in/varunwagle/)

-----------------------------------------------------------------------

# 🏁 Status

• ✅ Phase 1: Project Setup & Planning – Completed
• 🚀 Phase 2: Core Architecture Design – In Progress