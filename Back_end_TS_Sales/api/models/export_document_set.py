from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.models import BaseModel


class ExportDocumentSet(BaseModel):
    """ExportDocumentSet model - Export documents for shipment"""
    __tablename__ = "export_document_set"

    document_set_id = Column(Integer, primary_key=True, index=True)
    sale_order_id = Column(Integer, ForeignKey(
        "sale_order.sale_order_id"), nullable=False, index=True)
    issue_date = Column(Date, nullable=True)
    # B/L, Invoice, Packing List, Certificate of Origin, Health Certificate
    document_type = Column(String(50), nullable=True)
    file_path = Column(String(200), nullable=True)
    # COMPLETED, IN_PROGRESS, PENDING
    status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)

    # Relationships
    sale_order = relationship("SaleOrder", back_populates="export_documents")
