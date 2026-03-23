from sqlalchemy import Column, String, Date, Float, ForeignKey
from api.database import Base

class Contract(Base):
    __tablename__ = "contract"

    contract_id = Column(String(50), primary_key=True)

    customer_id = Column(String(50), ForeignKey("customer.customer_id"))
    payment_term_id = Column(String(50), ForeignKey("payment_term.payment_term_id"))

    proforma_invoice_id = Column(String(50), ForeignKey("proforma_invoice.proforma_invoice_id"))

    staff_id = Column(String(50), ForeignKey("staff.staff_id"))
    contract_type_id = Column(String(50), ForeignKey("contract_type.contract_type_id"))

    incoterm_id = Column(String(50), ForeignKey("incoterm.incoterm_id"))

    contract_date = Column(Date)
    effective_date = Column(Date)
    expiry_date = Column(Date)

    total_value = Column(Float)

    loading_port = Column(String(100))
    destination_port = Column(String(100))

    currency = Column(String(50))

    total_contract_value = Column(Float)
    total_quantity = Column(Float)

    status = Column(String(50))
    signed_date = Column(Date)