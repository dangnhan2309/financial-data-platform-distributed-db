from sqlalchemy import Column, String, Date, ForeignKey
from api.database import Base


class Shipment(Base):
    __tablename__ = "shipment"

    shipment_id = Column(String(50), primary_key=True)

    sale_order_id = Column(String(50), ForeignKey("sale_order.sale_order_id"))

    shipment_date = Column(Date)
    carrier = Column(String(200))
    tracking_number = Column(String(200))


class ExportDocumentSet(Base):
    __tablename__ = "export_document_set"

    document_set_id = Column(String(50), primary_key=True)

    shipment_id = Column(String(50), ForeignKey("shipment.shipment_id"))

    issue_date = Column(Date)
    status = Column(String(50))