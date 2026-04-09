"""SaleOrder Service - Business logic for SaleOrder"""
from api.repositories.sale_order_repository import SaleOrderRepository
from api.models import SaleOrder
from schemas.sale_order_schema import SaleOrderCreate, SaleOrderUpdate
from sqlalchemy.orm import Session
from datetime import date


class SaleOrderService:
    """Service layer for SaleOrder operations"""

    def __init__(self, db: Session):
        self.repository = SaleOrderRepository(db=db)
        self.db = db

    def create_sale_order(self, sale_order_data: SaleOrderCreate) -> SaleOrder:
        """Create new sale order"""
        db_sale_order = SaleOrder(**sale_order_data.dict())
        return self.repository.create(db_sale_order)

    def get_sale_order(self, sale_order_id: int) -> SaleOrder:
        """Get sale order by ID"""
        return self.repository.get_by_id(sale_order_id)

    def get_all_sale_orders(self, skip: int = 0, limit: int = 100) -> list:
        """Get all sale orders with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_sale_orders_by_contract(self, contract_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get sale orders by contract"""
        return self.repository.get_by_contract(contract_id, skip=skip, limit=limit)

    def get_sale_orders_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list:
        """Get sale orders by status"""
        return self.repository.get_by_status(status, skip=skip, limit=limit)

    def get_pending_sale_orders(self, skip: int = 0, limit: int = 100) -> list:
        """Get pending sale orders"""
        return self.repository.get_pending_orders(skip=skip, limit=limit)

    def get_completed_sale_orders(self, skip: int = 0, limit: int = 100) -> list:
        """Get completed sale orders"""
        return self.repository.get_completed_orders(skip=skip, limit=limit)

    def update_sale_order(self, sale_order_id: int, sale_order_data: SaleOrderUpdate) -> SaleOrder:
        """Update sale order"""
        db_sale_order = self.repository.get_by_id(sale_order_id)
        if db_sale_order:
            return self.repository.update(sale_order_id, sale_order_data.dict(exclude_unset=True))
        return None

    def delete_sale_order(self, sale_order_id: int) -> bool:
        """Delete sale order"""
        return self.repository.delete(sale_order_id)

    def get_sale_orders_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> list:
        """Get sale orders within date range"""
        return self.repository.get_by_date_range(start_date, end_date, skip=skip, limit=limit)
