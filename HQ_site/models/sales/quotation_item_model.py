class QuotationItem(Base):
    __tablename__ = "quotation_item"
    quotation_id = Column(String(50), ForeignKey("quotation.quotation_id"), primary_key=True)
    product_id = Column(String(50), ForeignKey("product.product_id"), primary_key=True)
    quantity = Column(Float)
    unit_price = Column(Float)
    discount = Column(Float)
    tax_rate = Column(Float)
    total_price = Column(Float)
    # PrimaryKeyConstraint('quotation_id', 'product_id') được hiểu ngầm qua primary_key=True ở 2 cột