class SaleOrder(Base):
    __tablename__ = "sale_order"
    sale_order_id = Column(String(50), primary_key=True)
    contract_id = Column(String(50), ForeignKey("contract.contract_id"))
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    total_amount = Column(Float)
    currency = Column(String(10))
    status = Column(String(20))