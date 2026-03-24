class Quotation(Base):
    __tablename__ = "quotation"
    quotation_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customer.customer_id"))
    staff_id = Column(String(50), ForeignKey("staff.staff_id"))
    quotation_date = Column(DateTime)
    expiry_date = Column(DateTime)
    incoterm_id = Column(String(50), ForeignKey("incoterm.incoterm_id"))
    payment_term_id = Column(String(50), ForeignKey("payment_term.payment_term_id"))
    total_amount = Column(Float)
    currency = Column(String(10))
    status = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())