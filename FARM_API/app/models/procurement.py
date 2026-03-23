from sqlalchemy import Column, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PurchaseContract(Base):
    __tablename__ = "purchase_contract"
    
    contract_id = Column(String, primary_key=True)
    supplier_id = Column(String, ForeignKey("supplier.supplier_id"))
    ingredient_id = Column(String, ForeignKey("ingredient.ingredient_id"))
    committed_quantity = Column(Float)
    contract_price = Column(Float)
    quality_commitment = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)
    
    supplier = relationship("Supplier", back_populates="contracts")
    ingredient = relationship("Ingredient", back_populates="purchase_contracts")
    batches = relationship("PurchaseBatch", back_populates="contract")

class PurchaseBatch(Base):
    __tablename__ = "purchase_batch"
    
    batch_id = Column(String, primary_key=True)
    contract_id = Column(String, ForeignKey("purchase_contract.contract_id"))
    purchase_date = Column(Date)
    expected_quantity = Column(Float)
    unit_price = Column(Float)
    status = Column(String)
    
    contract = relationship("PurchaseContract", back_populates="batches")
    tickets = relationship("PurchaseTicket", back_populates="batch")

class PurchaseTicket(Base):
    __tablename__ = "purchase_ticket"
    
    ticket_id = Column(String, primary_key=True)
    batch_id = Column(String, ForeignKey("purchase_batch.batch_id"))
    supplier_id = Column(String, ForeignKey("supplier.supplier_id"))
    ingredient_id = Column(String, ForeignKey("ingredient.ingredient_id"))
    raw_weight = Column(Float)
    received_at = Column(DateTime)
    
    batch = relationship("PurchaseBatch", back_populates="tickets")
    supplier = relationship("Supplier", back_populates="purchase_tickets")
    ingredient = relationship("Ingredient", back_populates="purchase_tickets")
    
    qc_receivings = relationship("QCReceiving", back_populates="purchase_ticket")


class ProductionLot(Base):
    __tablename__ = "production_lot"
    
    lot_id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("product.product_id"))
    mfg_date = Column(DateTime)
    exp_date = Column(DateTime)
    
    product = relationship("Product", back_populates="production_lots")
    qc_product_lots = relationship("QCProductLot", back_populates="production_lot")

