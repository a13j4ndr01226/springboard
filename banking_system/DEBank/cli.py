import sys 
from sqlalchemy.orm import Session
from .models.base import engine, SessionLocal, Base
from .models.customer import Customer
from .models.account import Account
from .models.transaction import Transaction
from .models.employee import Employee
from .utils.id_generator import generate_id
from datetime import datetime, timezone
from .utils.logger import logger


def main_menu():
    print("\n===== DE Bank =====")
    print("Choose User Interface")
    print("1. Customer (Self-Service)")
    print("2. Employee (Teller/Banker)")

    actor = input("Select (1 or 2): ").strip()
    role = "self"

    if actor == "2":
        role = input("Enter role (Teller/Banker): ").strip().lower()
        if role not in ["teller", "banker"]:
            print("Invalid role. Type in 'Teller' or 'Banker'")
            return

    banking_menu(role)

def banking_menu(role):
    while True:
        print("\n===== Main Menu =====")

        if role == "banker":
           options = [
                ("1", "Create Customer", create_customer),
                ("2", "Open Account", open_account),
                ("3", "Deposit", lambda: deposit(role)),
                ("4", "Withdraw", lambda: withdraw(role)),
                ("5", "Transfer Funds", lambda: transfer_funds(role)),
                ("6", "Submit Loan Application", lambda: submit_loan_application(role)),
                ("7", "View Account Info", view_account_info),
                ("8", "Exit", None)
            ]
        else:
            options = [
                ("3", "Deposit", lambda: deposit(role)),
                ("4", "Withdraw", lambda: withdraw(role)),
                ("5", "Transfer Funds", lambda: transfer_funds(role)),
                ("7", "View Account Info", view_account_info),
                ("8", "Exit", None)
            ]
        
        for key, label, _ in options:
            print(f"{key}. {label}")

        allowed = list(range(1, 9)) if role == "banker" else [3, 4, 5, 7, 8]
        choice = input("Select an option: ")

        if choice == "1" and 1 in allowed:
            create_customer()
        elif choice == "2" and 2 in allowed:
            open_account()
        elif choice == "3" and 3 in allowed:
            deposit(role)
        elif choice == "4" and 4 in allowed:
            withdraw(role)
        elif choice == "5" and 5 in allowed:
            transfer_funds(role)
        elif choice == "6" and 6 in allowed:
            submit_loan_application(role)
        elif choice == "7" and 7 in allowed:
            view_account_info()
        elif choice == "8" and 8 in allowed:
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")

def create_customer():
    session = SessionLocal()
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    customer = Customer(first_name=first, last_name=last)

    try:
        session.add(customer)
        session.commit()
    finally:
        print(f"Customer created with ID: {customer.customer_id}")
        session.close()
    
def open_account(customer=None):
    session = SessionLocal()
    try:
        if not customer:
            customer_id = input("Enter customer ID: ")
            customer = session.query(Customer).filter_by(customer_id=int(customer_id)).first()
            if not customer:
                print("Customer not found.")
                return

        account_type = input("Enter account type (checking/savings): ").lower()
        new_account = Account(account_type=account_type, customer_id=customer.customer_id)
        session.add(new_account)
        session.commit()
        print(f"{account_type.capitalize()} account opened with ID {new_account.account_id}")
    finally:
        session.close()

def deposit(role="self"):
    session = SessionLocal()
    customer_id = input("Enter customer ID: ")
    try:
        try:
            customer = session.query(Customer).filter_by(customer_id=int(customer_id)).first()
        except ValueError:
            print("Invalid customer ID.")
            return

        if not customer:
            print("Customer not found.")
            return

        if not customer.accounts:
            print("No accounts found for this customer.")
            create = input("Would you like to open an account? (Y/N): ").lower()
            if create == "y":
                open_account(customer)
                session.commit()
            else:
                return

        print("\nChoose account number:")
        for i, acc in enumerate(customer.accounts, start=1):
            print(f"[{i}] {acc.account_type} | ID: {acc.account_id} | Balance: ${acc.balance:.2f}")

        try:
            index = int(input("Select an account using number option: ")) - 1
            selected_account = customer.accounts[index]
        except (IndexError, ValueError):
            print("Invalid account selection.")
            return

        try:
            amount = float(input("Enter deposit amount: "))
            if amount <= 0:
                raise ValueError
        except ValueError:
            print("Deposit amount must be a positive number.")
            return

        # Perform deposit
        selected_account.balance += amount

        # Attach employee if applicable
        employee_id = None
        if role in ["teller", "banker"]:
            employee = session.query(Employee).filter_by(role=role).first()
            if employee:
                employee_id = employee.employee_id

        transaction = Transaction(
            transaction_id=generate_id(12),
            account_id=selected_account.account_id,
            transaction_type="deposit",
            amount=amount,
            employee_id=employee_id,
            performed_by=role,
            timestamp=datetime.now(timezone.utc)
        )

        session.add(transaction)
        session.commit()
        logger.info(f"{role.capitalize()} deposited ${amount:.2f} to Account {selected_account.account_id}")
        print(f"Deposited ${amount:.2f} into account {selected_account.account_id}")
        print(f"New Balance: ${selected_account.balance:.2f}")

    finally:
        session.close()

def withdraw(role="self"):
    session = SessionLocal()
    customer_id = input("Enter customer ID: ")

    customer = session.query(Customer).filter_by(customer_id=int(customer_id)).first()

    try:
        if not customer:
            print("Customer not found.")
            return

        if not customer.accounts:
            print("No accounts found for this customer.")
            return

        print("\nChoose account:")
        for i, acc in enumerate(customer.accounts, start=1):
            print(f"[{i}] {acc.account_type} | ID: {acc.account_id} | Balance: ${acc.balance:.2f}")

        try:
            index = int(input("Select an account using number option: ")) - 1
            selected_account = customer.accounts[index]
        except (IndexError, ValueError):
            print("Invalid account selection.")
            return

        try:
            amount = float(input("Enter withdrawal amount: "))
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return

        if amount > selected_account.balance:
            print("Insufficient funds.")
            return

        # Perform withdrawal
        selected_account.balance -= amount

        # Track who handled the transaction
        employee_id = None
        if role in ["teller", "banker"]:
            employee = session.query(Employee).filter_by(role=role).first()
            if employee:
                employee_id = employee.employee_id

        transaction = Transaction(
            transaction_id=generate_id(12),
            account_id=selected_account.account_id,
            transaction_type="withdrawal",
            amount=amount,
            employee_id=employee_id,
            performed_by=role,
            timestamp=datetime.now(timezone.utc)
        )

        session.add(transaction)
        session.commit()
        logger.info(f"{role.capitalize()} withdrew ${amount:.2f} from Account {selected_account.account_id}")
        print(f"Withdrew ${amount:.2f} from account {selected_account.account_id}")
        print(f"New Balance: ${selected_account.balance:.2f}")

    finally:
        session.close()

def transfer_funds(role):
    session = SessionLocal()
    from_id = int(input("Account Number to trasfer FROM: "))
    to_id = int(input("Account Number to deposit TO: "))

    from_account = session.query(Account).filter_by(account_id=from_id).first()
    to_account = session.query(Account).filter_by(account_id=to_id).first()

    try:

        if not from_account:
            print("Invalid FROM account.")
            return
        if not to_account:
            print("Invalid TO account.")
            return

        try:
            amount = float(input("Enter transfer amount: "))
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0:
            print("Transfer amount must be greater than zero.")
            return

        if from_account.balance < amount:
            print("Insufficient funds.")
            return

        from_account.balance -= amount
        to_account.balance += amount

        employee_id = None
        if role in ["teller", "banker"]:
            employee = session.query(Employee).filter_by(role=role).first()
            if employee:
                employee_id = employee.employee_id

        # Create transactions
        transaction_from = Transaction(
            transaction_id=generate_id(12),
            account_id=from_account.account_id,
            transaction_type="transfer_out",
            amount=amount,
            employee_id=employee_id,
            performed_by=role,
            timestamp=datetime.now(timezone.utc)
        )

        transaction_to = Transaction(
            transaction_id=generate_id(12),
            account_id=to_account.account_id,
            transaction_type="transfer_in",
            amount=amount,
            employee_id=employee_id,
            performed_by=role,
            timestamp=datetime.now(timezone.utc)
        )

        session.add_all([transaction_from, transaction_to])
        session.commit()
        logger.info(f"{role.capitalize()} transferred ${amount:.2f} from Account {from_id} to Account {to_id}")
        print(f"Transfer of ${amount:.2f} from {from_id} to {to_id} by {role} completed.")
    
    finally:
        session.close()

def submit_loan_application(role):
    if role != "banker":
        print("Access Denied. Banker must submit application.")
        return
    try:
        customer_id = int(input("Enter customer ID: "))
        amount = float(input("Enter loan amount: "))
        print(f"Loan application for ${amount:.2f} submitted for Customer {customer_id}. Status: Pending approval.")
    except ValueError:
        print("Invalid Input.")
        return

def view_account_info():
    session = SessionLocal()
    try:
        customer_id = input("Enter customer ID: ")
        customer = session.query(Customer).filter_by(customer_id=int(customer_id)).first()

        if not customer:
            print("Customer not found.")
            return

        print(f"\nCustomer Info:")
        print(f"Name: {customer.first_name} {customer.last_name}")
        print(f"Address: {customer.address or 'N/A'}")

        if not customer.accounts:
            print("This customer has no accounts.")
            return

        print("\nAccounts:")
        for acc in customer.accounts:
            print(f"- {acc.account_type.title()} | ID: {acc.account_id} | Balance: ${acc.balance:.2f}")

            # Show transaction history for this account
            if acc.transactions:
                print("  Transactions:")
                for txn in acc.transactions:
                    handler = f"Employee #{txn.employee_id}" if txn.employee_id else txn.performed_by
                    print(f"    [{txn.timestamp}] {txn.transaction_type.title()} - ${txn.amount:.2f} (Handled by {handler})")

            else:
                print("  No transactions found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        
    finally:
        session.close()

#Checks how file is being run. Allows to be executed as a script.
if __name__ == "__main__":
    main_menu()
