from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import Base

class Customer(Base):
    __tablename__ = "customer"
    
    customer_id = Column(String, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    loyalty_points = Column(Integer)
    
    orders = relationship("SalesOrder", back_populates="customer")

class SalesOrder(Base):
    __tablename__ = "sales_order"
    
    order_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"))
    
    order_date = Column(DateTime)
    status = Column(String) # 'PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'
    total_amount = Column(Float)
    shipping_address = Column(String)
    
    customer = relationship("Customer", back_populates="orders")
    items = relationship("SalesItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")

class SalesItem(Base):
    __tablename__ = "sales_item"
    
    item_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("sales_order.order_id"))
    product_id = Column(String, ForeignKey("product.product_id"))
    
    quantity = Column(Float)
    unit_price = Column(Float)
    subtotal = Column(Float)
    
    order = relationship("SalesOrder", back_populates="items")
    product = relationship("Product", back_populates="sales_items")

class Payment(Base):
    __tablename__ = "payment"
    
    payment_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("sales_order.order_id"))
    
    payment_method = Column(String)
    amount = Column(Float)
    payment_date = Column(DateTime)
    status = Column(String)
    
    order = relationship("SalesOrder", back_populates="payments")
