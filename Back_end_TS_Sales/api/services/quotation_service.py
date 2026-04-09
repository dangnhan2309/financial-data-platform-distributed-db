"""Quotation Service - Business logic for Quotation"""
from api.repositories.quotation_repository import QuotationRepository
from api.models import Quotation
from schemas.quotation_schema import QuotationCreate, QuotationUpdate
from sqlalchemy.orm import Session
from datetime import date


class QuotationService:
    """Service layer for Quotation operations"""

    def __init__(self, db: Session):
        self.repository = QuotationRepository(db=db)
        self.db = db

    def create_quotation(self, quotation_data: QuotationCreate) -> Quotation:
        """Create new quotation"""
        db_quotation = Quotation(**quotation_data.dict())
        return self.repository.create(db_quotation)

    def get_quotation(self, quotation_id: int) -> Quotation:
        """Get quotation by ID"""
        return self.repository.get_by_id(quotation_id)

    def get_all_quotations(self, skip: int = 0, limit: int = 100) -> list:
        """Get all quotations with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_quotations_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get quotations by customer"""
        return self.repository.get_by_customer(customer_id, skip=skip, limit=limit)

    def get_quotations_by_staff(self, staff_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get quotations by staff"""
        return self.repository.get_by_staff(staff_id, skip=skip, limit=limit)

    def get_quotations_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list:
        """Get quotations by status"""
        return self.repository.get_by_status(status, skip=skip, limit=limit)

    def get_active_quotations(self, skip: int = 0, limit: int = 100) -> list:
        """Get active quotations"""
        return self.repository.get_active_quotations(skip=skip, limit=limit)

    def update_quotation(self, quotation_id: int, quotation_data: QuotationUpdate) -> Quotation:
        """Update quotation"""
        db_quotation = self.repository.get_by_id(quotation_id)
        if db_quotation:
            return self.repository.update(quotation_id, quotation_data.dict(exclude_unset=True))
        return None

    def delete_quotation(self, quotation_id: int) -> bool:
        """Delete quotation"""
        return self.repository.delete(quotation_id)

    def get_quotations_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> list:
        """Get quotations within date range"""
        return self.repository.get_by_date_range(start_date, end_date, skip=skip, limit=limit)
