from sqlalchemy.orm import Session
from api.repositories import customer_repository
from api.models.customer import Customer
from api.utils.id_generator import generate_customer_id


def create_customer_service(db: Session, customer_data):

    customer_id = generate_customer_id()

    new_customer = Customer(
        customer_id=customer_id,
        **customer_data.dict()
    )

    return customer_repository.create_customer(db, new_customer)


def get_customer_service(db: Session, customer_id: str):

    customer = customer_repository.get_customer_by_id(db, customer_id)

    if not customer:
        raise ValueError("Customer not found")

    return customer


def get_all_customers_service(db: Session):
    return customer_repository.get_all_customers(db)