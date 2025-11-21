# Cafeteria Purchase Logger System

A Python-based cafeteria transaction logging system designed to improve purchase integrity and accountability by tracking student food purchases with comprehensive validation and fraud detection.

## 📋 Overview

This system addresses the problem of students taking food without proper payment verification. It provides:
- Student ID validation against a database
- Digital payment tracking by bank
- Automated fraud detection flags
- Daily transaction reports for management reconciliation

## ✨ Features

### Core Functionality
- **Student Validation**: Verifies student matric numbers against registered student database
- **Payment Logging**: Records transaction details including bank, amount, and timestamp
- **Multi-Bank Support**: Supports 20+ major Nigerian banks (GTBank, UBA, Access Bank, etc.)
- **Transaction History**: View complete purchase history with search and filtering

### Integrity & Security
- **Fraud Detection System**:
  - Flags purchases above ₦5,000
  - Detects rapid purchases (< 10 minutes apart)
  - Alerts when daily transaction limit exceeded (3 per day)
  - Identifies off-hours transactions (outside 6 AM - 11 PM)
- **Data Validation**:
  - Price range enforcement (₦100 - ₦10,000)
  - Required fields validation
  - Immutable transaction logs

### Management Tools
- **Daily Reconciliation**: Export transactions for bank statement cross-checking
- **Suspicious Activity Alerts**: Automatic flagging of unusual patterns
- **Audit Trail**: Complete timestamp and student information for every transaction

## 🛠️ Technical Stack

- **Language**: Python 3.13+
- **GUI Framework**: Tkinter
- **Database**: SQLite3
- **Libraries**: 
  - `sqlite3` - Database management
  - `tkinter` - User interface
  - `datetime` - Timestamp handling

## 📁 Project Structure

```
cafeteria-logger/
├── logger.py              # Main GUI application
├── data_handler.py        # Data validation and fraud detection logic
├── create_student_db.py   # Student database setup script
├── students.db            # Student records database
├── logger.db              # Transaction logs database
├── attendance.csv         # Student data import file (optional)
└── README.md             # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.13 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd cafeteria-logger
   ```

2. **Create the student database**
   
   First, prepare your student data in CSV format (`attendance.csv`):
   ```csv
   S/N,Name,Department,Matric_no
   1,John Doe,Computer Engineering,125/22/1/0001
   2,Jane Smith,Electrical Engineering,125/22/2/0002
   ```

   Then run:
   ```bash
   python create_student_db.py
   ```

3. **Run the application**
   ```bash
   python logger.py
   ```

## 💻 Usage

### For Cafeteria Staff

1. **Validate Student**
   - Enter student matric number
   - Click "Validate" button
   - System displays student name if valid

2. **Record Purchase**
   - Select payment bank from dropdown
   - Enter purchase amount (₦100 - ₦10,000)
   - Click "LOG" to record transaction
   - System shows warnings for suspicious activity

3. **View History**
   - Click "Show log history" to view all transactions
   - Flagged transactions are marked with ⚠️

### For Management

1. **Daily Reconciliation**
   - Review transaction logs in `logger.db` using SQLite viewer
   - Check flagged transactions for investigation
   - Cross-reference with bank statements

2. **Fraud Investigation**
   - Filter transactions by flags:
     - `HIGH_AMOUNT` - Purchases over ₦5,000
     - `RAPID_PURCHASE` - Multiple purchases within 10 minutes
     - `DAILY_LIMIT_REACHED` - More than 3 purchases per day
     - `OFF_HOURS` - Purchases outside operating hours

## 🗄️ Database Schema

### students.db
| Column     | Type | Description                    |
|------------|------|--------------------------------|
| matric     | TEXT | Student matric number (PRIMARY KEY) |
| name       | TEXT | Student full name              |
| department | TEXT | Student's department           |

### logger.db
| Column    | Type    | Description                           |
|-----------|---------|---------------------------------------|
| matric    | TEXT    | Student matric number                 |
| name      | TEXT    | Student name                          |
| bank      | TEXT    | Payment bank                          |
| price     | INTEGER | Purchase amount in Naira              |
| timestamp | TEXT    | ISO format timestamp                  |
| flags     | TEXT    | Comma-separated fraud detection flags |

## ⚙️ Configuration

Edit `data_handler.py` to customize settings:

```python
MIN_PRICE = 100                    # Minimum purchase amount
MAX_PRICE = 10000                  # Maximum purchase amount
CAFETERIA_OPEN = 6                 # Opening hour (24-hour format)
CAFETERIA_CLOSE = 23               # Closing hour (24-hour format)
MAX_DAILY_TRANSACTIONS = 3         # Maximum purchases per student per day
RAPID_PURCHASE_MINUTES = 10        # Minimum minutes between purchases
```

## 🔒 Security Features

- **Validation Before Logging**: Students must be validated before transactions can be recorded
- **Immutable Logs**: Transaction records cannot be modified after creation
- **Fraud Detection**: Automatic flagging of suspicious patterns
- **Audit Trail**: Complete timestamp and student information for accountability

## �
