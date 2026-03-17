from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base


class Product(Base):
    __tablename__ = "product"

    product_id = Column(String(50), primary_key=True)
    product_type_id = Column(String(50), ForeignKey("product_type.product_type_id"))

    name = Column(String(200))
    description = Column(String(500))
    price = Column(Float)

    application = Column(String(200))
    brix = Column(String(50))
    size = Column(String(50))
    solid = Column(Float)
    ph = Column(Float)

    is_active = Column(Integer)


class IngredientProductDetail(Base):
    __tablename__ = "ingredient_product_detail"

    ingredient_id = Column(String(50), ForeignKey("ingredient.ingredient_id"), primary_key=True)
    product_id = Column(String(50), ForeignKey("product.product_id"), primary_key=True)

    quantity = Column(Float)
    unit_of_measure = Column(String(50))


class ProductSpecification(Base):
    __tablename__ = "product_specification"

    product_specification_id = Column(String(50), primary_key=True)

    product_id = Column(String(50), ForeignKey("product.product_id"))
    packaging_id = Column(String(50), ForeignKey("packaging_specification.packaging_id"))
    certification_id = Column(String(50), ForeignKey("certification.certification_id"))
    quality_assurance_id = Column(String(50), ForeignKey("quality_assurance.quality_assurance_id"))

    shelf_life_days = Column(Integer)
    storage_condition = Column(String(200))
    origin = Column(String(200))