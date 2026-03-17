from pydantic import BaseModel
from datetime import date


class ShipmentBase(BaseModel):
    sale_order_id: str
    shipment_date: date
    carrier: str
    tracking_number: str


class ShipmentCreate(ShipmentBase):
    shipment_id: str


class ShipmentResponse(ShipmentBase):
    shipment_id: str

    class Config:
        from_attributes = True


class ExportDocumentSetBase(BaseModel):
    shipment_id: str
    issue_date: date
    status: str


class ExportDocumentSetCreate(ExportDocumentSetBase):
    document_set_id: str


class ExportDocumentSetResponse(ExportDocumentSetBase):
    document_set_id: str

    class Config:
        from_attributes = True