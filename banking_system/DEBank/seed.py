from .models.base import engine, SessionLocal, Base
from .models.employee import Employee
from .models.service import Service
from .utils.id_generator import generate_id

def seed_data():
    session = SessionLocal()

    # Create 1 employee per role
    employees = [
        Employee(employee_id=generate_id(9), first_name="Alex", last_name="Jameson", role="teller"),
        Employee(employee_id=generate_id(9), first_name="Michael", last_name="LaCroix", role="banker"),
        Employee(employee_id=generate_id(9), first_name="Carol", last_name="Lee", role="manager")
    ]

    # Create 3 basic services
    services = [
        Service(service_id=generate_id(2), description="Transfer Funds"),
        Service(service_id=generate_id(2), description="Submit Loan Application"),
    ]

    session.add_all(employees + services)
    session.commit()
    print("Seed data inserted.")

#Checks how file is being run. Allows to be executed as a script.
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    seed_data()
