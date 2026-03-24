class Certification(Base):
    __tablename__ = "certification"
    certification_id = Column(String(50), primary_key=True)
    name = Column(String(255))
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    issued_by = Column(String(255))
    status = Column(String(50))
    description = Column(String(500))