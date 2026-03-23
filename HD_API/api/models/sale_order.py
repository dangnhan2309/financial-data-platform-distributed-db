from sqlalchemy import Column, String, Date, Float, ForeignKey
from api.database import Base


class SaleOrder(Base):
    __tablename__ = "sale_order"

    sale_order_id = Column(String(50), primary_key=True)

    contract_id = Column(String(50), ForeignKey("contract.contract_id"))

    order_date = Column(Date)
    delivery_date = Column(Date)

    total_amount = Column(Float)