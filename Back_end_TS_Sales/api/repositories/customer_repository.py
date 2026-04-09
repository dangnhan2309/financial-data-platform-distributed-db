"""Customer Repository - Database operations for Customer"""
from api.repositories.base_repository import BaseRepository
from api.models import Customer
from sqlalchemy.orm import Session


class CustomerRepository(BaseRepository[Customer]):
    """Repository for Customer model operations"""

    def __init__(self, db: Session):
        super().__init__(db=db, model=Customer)

    def get_by_customer_code(self, customer_code: str) -> Customer:
        """Get customer by customer code"""
        return self.db.query(self.model).filter(
            self.model.customer_code == customer_code
        ).first()

    def get_by_email(self, email: str) -> Customer:
        """Get customer by email"""
        return self.db.query(self.model).filter(
            self.model.email == email
        ).first()

    def get_active_customers(self, skip: int = 0, limit: int = 100) -> list:
        """Get active customers only"""
        return self.db.query(self.model).filter(
            self.model.status == "ACTIVE"
        ).offset(skip).limit(limit).all()
