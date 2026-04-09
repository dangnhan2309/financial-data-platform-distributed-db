"""Quotation Repository - Database operations for Quotation"""
from api.repositories.base_repository import BaseRepository
from api.models import Quotation
from sqlalchemy.orm import Session
from datetime import datetime, date


class QuotationRepository(BaseRepository[Quotation]):
    """Repository for Quotation model operations"""

    def __init__(self, db: Session):
        super().__init__(db=db, model=Quotation)

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get quotations for a customer"""
        return self.db.query(self.model).filter(
            self.model.customer_id == customer_id
        ).offset(skip).limit(limit).all()

    def get_by_staff(self, staff_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get quotations created by a staff"""
        return self.db.query(self.model).filter(
            self.model.staff_id == staff_id
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list:
        """Get quotations by status (DRAFT, APPROVED, REJECTED, EXPIRED, PENDING_REVIEW)"""
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()

    def get_active_quotations(self, skip: int = 0, limit: int = 100) -> list:
        """Get non-expired quotations"""
        return self.db.query(self.model).filter(
            self.model.expiry_date >= date.today()
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> list:
        """Get quotations within date range"""
        return self.db.query(self.model).filter(
            self.model.quotation_date >= start_date,
            self.model.quotation_date <= end_date
        ).offset(skip).limit(limit).all()
