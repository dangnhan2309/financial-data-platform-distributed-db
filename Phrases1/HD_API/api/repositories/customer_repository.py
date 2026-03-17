from sqlalchemy.orm import Session
from api.models.customer import Customer


def create_customer(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer_by_id(db: Session, customer_id: str):
    return db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()


def get_all_customers(db: Session):
    return db.query(Customer).all()


def update_customer(db: Session, customer: Customer):
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: Customer):
    db.delete(customer)
    db.commit()