from sqlalchemy import Column, String, Date, Float, ForeignKey
from api.database import Base


class Quotation(Base):
    __tablename__ = "quotation"

    quotation_id = Column(String(50), primary_key=True)

    customer_id = Column(String(50), ForeignKey("customer.customer_id"))
    staff_id = Column(String(50), ForeignKey("staff.staff_id"))

    quotation_date = Column(Date)
    expiry_date = Column(Date)

    incoterm_id = Column(String(50), ForeignKey("incoterm.incoterm_id"))
    payment_term_id = Column(String(50), ForeignKey("payment_term.payment_term_id"))


class QuotationItem(Base):
    __tablename__ = "quotation_item"

    quotation_id = Column(String(50), ForeignKey("quotation.quotation_id"), primary_key=True)
    product_id = Column(String(50), ForeignKey("product.product_id"), primary_key=True)

    quantity = Column(Float)
    unit_price = Column(Float)