class QualityAssurance(Base):
    __tablename__ = "quality_assurance"
    quality_assurance_id = Column(String(50), primary_key=True)
    name = Column(String(255))
    description = Column(String(500))
    standard_reference = Column(String(255))
    status = Column(String(50))