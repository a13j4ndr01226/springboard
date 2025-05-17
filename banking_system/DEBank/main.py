from .models import Base, Customer, Account, Transaction, Employee, Service
from .models.base import engine

# Create tables in the database
def init_db():
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")

#Checks how file is being run. Allows to be executed as a script.
if __name__ == "__main__":
    init_db()
