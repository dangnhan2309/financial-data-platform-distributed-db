class Factory(Base):
    __tablename__ = "factory"
    factory_id = Column(String(50), primary_key=True)
    company_id = Column(String(50), ForeignKey("company.company_id"))
    name = Column(String(255))
    address = Column(String(500))
    country = Column(String(100))
    status = Column(String(20))