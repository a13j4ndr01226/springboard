from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship #sets up object-level relationships
from .base import Base
from ..utils.id_generator import generate_id

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, default= lambda: generate_id(7))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String)

    accounts = relationship("Account", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer(id = {self.customer_id}, name={self.first_name} {self.last_name})>"