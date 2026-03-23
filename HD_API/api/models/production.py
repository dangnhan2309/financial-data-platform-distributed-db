from sqlalchemy import Column, String, Date, Integer, ForeignKey
from api.database import Base


class ProductionLot(Base):
    __tablename__ = "production_lot"

    production_lot_id = Column(String(50), primary_key=True)
    factory_id = Column(String(50), ForeignKey("factory.factory_id"))
    product_id = Column(String(50), ForeignKey("product.product_id"))

    production_date = Column(Date)
    expiry_date = Column(Date)

    status = Column(Integer)


class CertificateOfAnalysis(Base):
    __tablename__ = "certificate_of_analysis"

    certificate_of_analysis_id = Column(String(50), primary_key=True)

    lot_id = Column(String(50), ForeignKey("production_lot.production_lot_id"))
    issue_date = Column(Date)   