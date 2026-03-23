from sqlalchemy import Column, String, Date, Float, ForeignKey
from api.database import Base


class Payment(Base): # OBJECT -> CỦA THỰC THỂ PAYMENT
    __tablename__ = "payment"

    payment_id = Column(String(50), primary_key=True)

    payment_term_id = Column(String(50), ForeignKey("payment_term.payment_term_id"))
    sale_order_id = Column(String(50), ForeignKey("sale_order.sale_order_id"))

    payment_date = Column(Date)
    amount = Column(Float)