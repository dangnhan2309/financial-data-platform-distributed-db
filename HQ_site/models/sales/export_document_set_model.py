class ExportDocumentSet(Base):
    __tablename__ = "export_document_set"
    document_set_id = Column(String(50), primary_key=True)
    shipment_id = Column(String(50), ForeignKey("shipment.shipment_id"))
    issue_date = Column(DateTime)
    document_type = Column(String(100)) # Ví dụ: Bill of Lading, Packing List
    file_path = Column(String(500))
    status = Column(String(20)) 