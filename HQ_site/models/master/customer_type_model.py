
class CustomerType(Base):
    __tablename__ = "customer_type"
    customer_type_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    status = Column(String(20))