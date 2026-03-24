from core.database import Base
from sqlalchemy import Column, String, Integer
class CompanyType(Base):
    __tablename__ = "company_type"
    company_type_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(String(20))