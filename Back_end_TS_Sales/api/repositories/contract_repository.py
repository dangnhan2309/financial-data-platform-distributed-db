"""Contract Repository - Database operations for Contract"""
from api.repositories.base_repository import BaseRepository
from api.models import Contract
from sqlalchemy.orm import Session
from datetime import date


class ContractRepository(BaseRepository[Contract]):
    """Repository for Contract model operations"""

    def __init__(self, db: Session):
        super().__init__(db=db, model=Contract)

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get contracts for a customer"""
        return self.db.query(self.model).filter(
            self.model.customer_id == customer_id
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list:
        """Get contracts by status (ACTIVE, EXPIRED, PENDING, COMPLETED, CANCELLED)"""
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()

    def get_active_contracts(self, skip: int = 0, limit: int = 100) -> list:
        """Get active contracts only"""
        return self.db.query(self.model).filter(
            self.model.status == "ACTIVE"
        ).offset(skip).limit(limit).all()

    def get_expired_contracts(self, skip: int = 0, limit: int = 100) -> list:
        """Get expired contracts"""
        return self.db.query(self.model).filter(
            self.model.expiry_date < date.today()
        ).offset(skip).limit(limit).all()

    def get_by_type(self, contract_type: str, skip: int = 0, limit: int = 100) -> list:
        """Get contracts by type (Standard, Long-term, Trial, Partnership)"""
        return self.db.query(self.model).filter(
            self.model.contract_type == contract_type
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> list:
        """Get contracts within date range"""
        return self.db.query(self.model).filter(
            self.model.contract_date >= start_date,
            self.model.contract_date <= end_date
        ).offset(skip).limit(limit).all()
