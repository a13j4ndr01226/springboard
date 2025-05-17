
import pytest
from datetime import datetime, timezone
from DEBank.models.customer import Customer
from DEBank.models.account import Account
from DEBank.models.transaction import Transaction
from DEBank.utils.id_generator import generate_id

def test_customer_creation():
    customer = Customer(first_name="Jane", last_name="Doe")
    assert customer.first_name == "Jane"
    assert customer.last_name == "Doe"

def test_account_creation_and_balance():
    customer = Customer(first_name="John", last_name="Smith")
    account = Account(customer_id=generate_id(7), account_type="checking")
    assert account.balance == 0.0
    account.deposit(100.0)
    assert account.balance == 100.0
    account.withdraw(30.0)
    assert account.balance == 70.0

def test_transaction_model():
    transaction = Transaction(
        transaction_id=generate_id(12),
        account_id=1234567890,
        transaction_type="deposit",
        amount=150.00,
        employee_id=None,
        performed_by="self",
        timestamp=datetime.now(timezone.utc)
    )
    assert transaction.transaction_type == "deposit"
    assert transaction.amount == 150.00
    assert transaction.performed_by == "self"
