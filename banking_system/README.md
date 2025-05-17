# Simple Banking System (CLI-based)

This is a basic command-line banking system built with Python and SQLAlchemy. It's meant to simulate simple banking operations like deposits, withdrawals, transfers, and more. It also includes employee roles like Teller and Banker, and tracks who performs each action.

---

## What This Project Does

- Lets customers:
- Deposit money
- Withdraw money
- Transfer money between accounts
- View their account info

- Lets employees:
- **Teller**: Same as customer, but their name is logged in the system
- **Banker**: Can do everything a Teller can, plus:
    - Create new customers
    - Open new accounts
    - Submit loan applications

- Every action gets logged in a **transactions table**, so you can see who did what and when.

---

## Project Structure

banking_system/                     
│
├── DEBank/                           #Main package
│   ├── __init__.py
│   ├── main.py                     
│   ├── seed.py
│   ├── cli.py                     
│   ├── models/                       
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── base.py
│   │   ├── customer.py
│   │   ├── employee.py
│   │   ├── service.py
│   │   └── transaction.py
│   ├── utils/                       # Utilities and helpers
│   │   ├── __init__.py
│   │   ├── id_generator.py
│   │   └── logger.py 
│   └── db/                         # Database storage
│   │   └── bank.db 
│   └── logs/                        # Log output directory
│       └── banking.log                 
│
├── tests/                          
│   ├── __init__.py
│   └── test_example.py             
│
├── requirements.txt                
├── LICENSE                         
├── README.md                       
└── .gitignore  
---

## How to Use It

1. **Clone this repo**:
   git clone https://github.com/your-username/simple-banking-system.git
   cd simple-banking-system

2. **Set up the virtual environment (optional but recommended)**:
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

3. **Install dependencies**:
    pip install -r requirements.txt

4. **Create the database**:
    python DEBank/main.py

5. **Seed it with employees and services**:
    python DEBank/seed.py

6. **Run the program**:
    python DEBank/cli.py

---

## Roles Explained

Customer
- Can deposit, withdraw, transfer funds, and view account info

Teller
- Similar to customer, but their actions are logged as performed by them (not “self-service”)

Banker
- Can perform all services including customer creation, open accounts, and submit loan applications

---

## Resetting the Database
If needed:

1. Delete the database file 
    rm DEBank/db/bank.db

2. Then recreate it:
    python DEBank/main.py
    python DEBank/seed.py

---

## Dependencies
This project uses:
    - Python 3.10+
    - SQLAlchemy (ORM for handling database stuff)

Install everything with:
    pip install -r requirements.txt

---

## License
This project is licensed under the [MIT License](LICENSE).

