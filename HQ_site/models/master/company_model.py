class Company(Base):
    __tablename__ = "company"
    company_id = Column(String(50), primary_key=True)
    company_type_id = Column(String(50), ForeignKey("company_type.company_type_id"))
    name = Column(String(255), nullable=False)
    short_name = Column(String(100))
    tax_id = Column(String(50))
    address = Column(String(500))
    country = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    status = Column(String(20))