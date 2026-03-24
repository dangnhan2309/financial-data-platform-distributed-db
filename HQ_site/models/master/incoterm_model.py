class Incoterm(Base):
    __tablename__ = "incoterm"
    incoterm_id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(500))
    version = Column(String(20))
    status = Column(String(20))