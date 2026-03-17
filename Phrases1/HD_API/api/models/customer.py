from sqlalchemy import Column, String, ForeignKey
from api.database import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(String(50), primary_key=True)
    customer_type_id = Column(String(50), ForeignKey("customer_type.customer_type_id"))

    customer_code = Column(String(50))
    company_name = Column(String(200))
    short_name = Column(String(100))
    tax_id = Column(String(100))

    country = Column(String(100))
    city = Column(String(100))
    address = Column(String(300))

    phone = Column(String(50))
    email = Column(String(200))
    website = Column(String(200))

    industry = Column(String(200))
    status = Column(String(50))
    preferred_currency = Column(String(50))