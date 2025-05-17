from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship #sets up object-level relationships
from .base import Base
from .transaction import Transaction

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  #'teller', 'banker', 'manager'

    transactions = relationship(Transaction, back_populates="employee")

    def __repr__(self):
        return (
            f"<Employee(id={self.employee_id}, name={self.first_name} {self.last_name}, role={self.role})>"
        )
