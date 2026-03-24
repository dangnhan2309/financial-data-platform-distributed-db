class ContactPerson(Base):
    __tablename__ = "contact_person"
    contact_person_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customer.customer_id"))
    name = Column(String(255))
    email = Column(String(100))
    phone = Column(String(20))
    position = Column(String(100))
    status = Column(String(20))