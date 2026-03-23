from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Ingredient(Base):
    __tablename__ = "ingredient"
    
    ingredient_id = Column(String, primary_key=True)
    name = Column(String)
    
    # Relationships
    harvest_tickets = relationship("WeighingTicket", back_populates="ingredient")
    purchase_contracts = relationship("PurchaseContract", back_populates="ingredient")
    purchase_tickets = relationship("PurchaseTicket", back_populates="ingredient")
    # inventory_items removed as Inventory now uses generic item_id
    products = relationship("Product", back_populates="ingredient")

class Product(Base):
    __tablename__ = "product"
    
    product_id = Column(String, primary_key=True)
    product_name = Column(String, nullable=True)
    ingredient_id = Column(String, ForeignKey("ingredient.ingredient_id"), nullable=True)
    
    ingredient = relationship("Ingredient", back_populates="products")
    production_lots = relationship("ProductionLot", back_populates="product")
    sales_items = relationship("SalesItem", back_populates="product")


