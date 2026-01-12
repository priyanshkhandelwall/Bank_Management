💼 Bank Management System (Python + Tkinter)

🧾 Overview
This project is a desktop-based Bank Management System developed using Python and Tkinter. It replicates essential banking operations such as account creation, authentication, deposits, withdrawals, balance inquiries, and administrative controls through an intuitive graphical interface.

The system relies on a structured file-based database to manage customer and admin records, prioritising correctness, simplicity, and clear separation between business logic and UI.

---

✨ Key Features

🔑 Role-Based Access
Dedicated login workflows for Admin and Customer users with secure credential validation.

🏦 Customer Account Management
Create, view, update, and close customer accounts with consistent data formatting.

💳 Transaction Processing
Deposit and withdrawal functionality with enforced minimum balance constraints.

📊 Account Summary
Display comprehensive account details including balance, personal information, and KYC status.

🗂️ Persistent Storage
File-based data persistence using structured text files for reliability and transparency.

🖥️ Desktop GUI
Clean, user-friendly desktop interface built using Tkinter.

---

🧩 System Architecture
The application is organised into clearly defined components:

Backend Logic
Handles authentication, validation, transactions, and file operations.

GUI Modules
Tkinter windows for login screens, admin dashboard, customer dashboard, and actions.

Database Layer
Text-file based storage with fixed-length records to maintain data integrity.

---

⚙️ Getting Started

Prerequisites
- Python 3.x
- Tkinter (included with standard Python installations)

---

📦 Installation

- Clone the repository
- git clone https://github.com/yourusername/bank-management-system.git
- cd bank-management-system
- Required directories are created automatically on first run:
  ./database/Admin
  ./database/Customer
  ./images

---

▶️ Running the Application

- Start the application:
  python bank_management.py
- Default Admin Credentials:
  Admin ID: admin
  Password: admin@123
- Workflow:
  Log in as Admin
  Create customer accounts
  Log out
- Log in as Customer using Account Number and PIN

---

📄 License
This project was developed for academic and learning purposes.

---
