"""Product Repository - Database operations for Product"""
from api.repositories.base_repository import BaseRepository
from api.models import Product
from sqlalchemy.orm import Session


class ProductRepository(BaseRepository[Product]):
    """Repository for Product model operations"""

    def __init__(self, db: Session):
        super().__init__(db=db, model=Product)

    def get_by_name(self, name: str) -> Product:
        """Get product by name"""
        return self.db.query(self.model).filter(
            self.model.name == name
        ).first()

    def get_active_products(self, skip: int = 0, limit: int = 100) -> list:
        """Get active products only"""
        return self.db.query(self.model).filter(
            self.model.is_active == 1
        ).offset(skip).limit(limit).all()

    def get_by_type(self, product_type: str, skip: int = 0, limit: int = 100) -> list:
        """Get products by type (Juice, Puree, Concentrate)"""
        return self.db.query(self.model).filter(
            self.model.product_type == product_type
        ).offset(skip).limit(limit).all()

    def get_by_price_range(self, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> list:
        """Get products within price range"""
        return self.db.query(self.model).filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).offset(skip).limit(limit).all()
