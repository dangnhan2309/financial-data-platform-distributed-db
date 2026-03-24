class ContractItem(Base):
    __tablename__ = "contract_item"
    contract_id = Column(String(50), ForeignKey("contract.contract_id"), primary_key=True)
    product_id = Column(String(50), ForeignKey("product.product_id"), primary_key=True)
    quantity = Column(Float)
    unit_price = Column(Float)
    discount = Column(Float)
    tax_rate = Column(Float)
    total_price = Column(Float)