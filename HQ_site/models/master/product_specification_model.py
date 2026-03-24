class ProductSpecification(Base):
    __tablename__ = "product_specification"
    product_specification_id = Column(String(50), primary_key=True)
    product_id = Column(String(50), ForeignKey("product.product_id"))
    packaging_id = Column(String(50), ForeignKey("packaging_specification.packaging_id"))
    certification_id = Column(String(50), ForeignKey("certification.certification_id"))
    quality_assurance_id = Column(String(50), ForeignKey("quality_assurance.quality_assurance_id"))
    shelf_life_days = Column(Integer)
    storage_condition = Column(String(255))
    origin = Column(String(100))
    status = Column(String(50))