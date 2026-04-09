"""Customer Service - Business logic for Customer"""
from api.repositories.customer_repository import CustomerRepository
from api.models import Customer
from schemas.customer_schema import CustomerCreate, CustomerUpdate
from sqlalchemy.orm import Session


class CustomerService:
    """Service layer for Customer operations"""

    def __init__(self, db: Session):
        self.repository = CustomerRepository(db=db)
        self.db = db

    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create new customer"""
        db_customer = Customer(**customer_data.dict())
        return self.repository.create(db_customer)

    def get_customer(self, customer_id: int) -> Customer:
        """Get customer by ID"""
        return self.repository.get_by_id(customer_id)

    def get_all_customers(self, skip: int = 0, limit: int = 100) -> list:
        """Get all customers with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_active_customers(self, skip: int = 0, limit: int = 100) -> list:
        """Get active customers"""
        return self.repository.get_active_customers(skip=skip, limit=limit)

    def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> Customer:
        """Update customer"""
        db_customer = self.repository.get_by_id(customer_id)
        if db_customer:
            return self.repository.update(customer_id, customer_data.dict(exclude_unset=True))
        return None

    def delete_customer(self, customer_id: int) -> bool:
        """Delete customer"""
        return self.repository.delete(customer_id)

    def get_customer_by_code(self, customer_code: str) -> Customer:
        """Get customer by customer code"""
        return self.repository.get_by_customer_code(customer_code)

    def get_customer_by_email(self, email: str) -> Customer:
        """Get customer by email"""
        return self.repository.get_by_email(email)

    def search_customers(self, **filters) -> list:
        """Search customers by filters"""
        return self.repository.get_by_filter(**filters)
