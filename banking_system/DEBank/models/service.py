from sqlalchemy import Column, Integer, String
from .base import Base
from ..utils.id_generator import generate_id

class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, default=lambda: generate_id(2))
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"<Service(id={self.service_id}, description='{self.description}')>"
