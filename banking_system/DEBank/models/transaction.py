from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from ..utils.id_generator import generate_id

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, default=lambda: generate_id(12))
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    performed_by = Column(String)  # 'self', 'teller', or 'banker'
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # account = relationship(Account, back_populates="transactions")
    # employee = relationship(Employee, back_populates="transactions")

    
    account = relationship("Account", back_populates="transactions")
    employee = relationship("Employee", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, type='{self.transaction_type}', account={self.account_id}, employee={self.employee_id}, amount={self.amount})>"
