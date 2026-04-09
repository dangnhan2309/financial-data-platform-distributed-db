"""SaleOrder Repository - Database operations for SaleOrder"""
from api.repositories.base_repository import BaseRepository
from api.models import SaleOrder
from sqlalchemy.orm import Session
from datetime import date


class SaleOrderRepository(BaseRepository[SaleOrder]):
    """Repository for SaleOrder model operations"""

    def __init__(self, db: Session):
        super().__init__(db=db, model=SaleOrder)

    def get_by_contract(self, contract_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get sale orders for a contract"""
        return self.db.query(self.model).filter(
            self.model.contract_id == contract_id
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list:
        """Get sale orders by status (DRAFT, PENDING, IN_PROGRESS, DELIVERED, COMPLETED, CANCELLED)"""
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()

    def get_pending_orders(self, skip: int = 0, limit: int = 100) -> list:
        """Get pending sale orders"""
        return self.db.query(self.model).filter(
            self.model.status.in_(["DRAFT", "PENDING", "IN_PROGRESS"])
        ).offset(skip).limit(limit).all()

    def get_completed_orders(self, skip: int = 0, limit: int = 100) -> list:
        """Get completed sale orders"""
        return self.db.query(self.model).filter(
            self.model.status == "COMPLETED"
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> list:
        """Get sale orders within date range"""
        return self.db.query(self.model).filter(
            self.model.order_date >= start_date,
            self.model.order_date <= end_date
        ).offset(skip).limit(limit).all()
