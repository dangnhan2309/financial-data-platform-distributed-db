class Staff(Base):
    __tablename__ = "staff"
    staff_id = Column(String(50), primary_key=True)
    name = Column(String(255))
    role = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    department = Column(String(100))
    status = Column(String(20))