"""Product Service - Business logic for Product"""
from api.repositories.product_repository import ProductRepository
from api.models import Product
from schemas.product_schema import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session


class ProductService:
    """Service layer for Product operations"""

    def __init__(self, db: Session):
        self.repository = ProductRepository(db=db)
        self.db = db

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create new product"""
        db_product = Product(**product_data.dict())
        return self.repository.create(db_product)

    def get_product(self, product_id: int) -> Product:
        """Get product by ID"""
        return self.repository.get_by_id(product_id)

    def get_all_products(self, skip: int = 0, limit: int = 100) -> list:
        """Get all products with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_active_products(self, skip: int = 0, limit: int = 100) -> list:
        """Get active products"""
        return self.repository.get_active_products(skip=skip, limit=limit)

    def get_products_by_type(self, product_type: str, skip: int = 0, limit: int = 100) -> list:
        """Get products by type"""
        return self.repository.get_by_type(product_type, skip=skip, limit=limit)

    def get_products_by_price_range(self, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> list:
        """Get products by price range"""
        return self.repository.get_by_price_range(min_price, max_price, skip=skip, limit=limit)

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Update product"""
        db_product = self.repository.get_by_id(product_id)
        if db_product:
            return self.repository.update(product_id, product_data.dict(exclude_unset=True))
        return None

    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        return self.repository.delete(product_id)

    def search_products(self, **filters) -> list:
        """Search products by filters"""
        return self.repository.get_by_filter(**filters)
