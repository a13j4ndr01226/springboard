from sqlalchemy import Column, Integer, Float, String, ForeignKey 
from sqlalchemy.orm import relationship #sets up object-level relationships
from .base import Base
from ..utils.id_generator import generate_id

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, default= lambda: generate_id(10))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable = False)
    
    """This sets up the ORM-level relationship (not stored in DB directly):

        Allows account.customer to give you the linked Customer object

        Matches the .accounts relationship on the Customer class"""
    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def __init__(self, customer_id, account_type, balance=0.0):
        self.customer_id = customer_id
        self.account_type = account_type
        self.balance = balance

    def __repr__(self):
        return (
            f"<Account(id={self.account_id}, type='{self.account_type}', "
            f"balance={self.balance}, customer_id={self.customer_id})>"
        )
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount: float):
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Invalid withdrawal amount.")


