from pydantic import BaseModel
from datetime import date


class ProductionLotBase(BaseModel):
    factory_id: str
    product_id: str
    production_date: date
    expiry_date: date
    status: int

class ProductionLotCreate(ProductionLotBase):
    production_lot_id: str


class ProductionLotResponse(ProductionLotBase):
    production_lot_id: str

    class Config:
        from_attributes = True


class CertificateOfAnalysisBase(BaseModel):
    lot_id: str
    issue_date: date


class CertificateOfAnalysisCreate(CertificateOfAnalysisBase):
    certificate_of_analysis_id: str


class CertificateOfAnalysisResponse(CertificateOfAnalysisBase):
    certificate_of_analysis_id: str

    class Config:
        from_attributes = True