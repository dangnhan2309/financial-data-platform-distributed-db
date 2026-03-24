class PackagingSpecification(Base):
    __tablename__ = "packaging_specification"
    packaging_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    unit_of_measure = Column(String(50))
    volume = Column(Float)
    material = Column(String(100))
    description = Column(String(500))
    is_active = Column(Integer, default=1)