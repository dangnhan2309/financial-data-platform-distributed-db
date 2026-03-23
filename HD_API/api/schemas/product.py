#from pydantic import BaseModel
from api.database import Base
from typing import Optional


class ProductBase(Base):
    product_type_id: str
    name: str
    description: Optional[str]
    price: float
    apilication: Optional[str]
    brix: Optional[str]
    size: Optional[str]
    solid: Optional[float]
    ph: Optional[float]
    is_active: int


class ProductCreate(ProductBase):
    product_id: str


class ProductResponse(ProductBase):
    product_id: str

    class Config:
        from_attributes = True


class IngredientProductDetailBase(Base):
    ingredient_id: str
    product_id: str
    quantity: float
    unit_of_measure: str


class IngredientProductDetailCreate(IngredientProductDetailBase):
    pass


class IngredientProductDetailResponse(IngredientProductDetailBase):

    class Config:
        from_attributes = True