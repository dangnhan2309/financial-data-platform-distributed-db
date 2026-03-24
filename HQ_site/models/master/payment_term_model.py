class PaymentTerm(Base):
    __tablename__ = "payment_term"
    payment_term_id = Column(String(50), primary_key=True)
    description = Column(String(500))
    number_of_days = Column(Integer)
    status = Column(String(20))