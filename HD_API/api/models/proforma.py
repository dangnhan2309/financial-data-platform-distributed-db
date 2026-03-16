from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from api.database import Base


class ProformaInvoice(Base):
    __tablename__ = "proforma_invoice"

    proforma_invoice_id = Column(String(50), primary_key=True)

    quotation_id = Column(
        String(50),
        ForeignKey("quotation.quotation_id"),
        nullable=False
    )

    payment_term_id = Column(
        String(50),
        ForeignKey("payment_term.payment_term_id")
    )

    bank_id = Column(
        String(50),
        ForeignKey("bank.bank_id")
    )

    staff_id = Column(
        String(50),
        ForeignKey("staff.staff_id")
    )

    total_contract_value = Column(Float)

    port_of_loading = Column(String(100))
    port_of_discharge = Column(String(100))

    delivery_time = Column(Date)

    file_path = Column(String(500))

    # Relationships
    quotation = relationship("Quotation", backref="proforma_invoices")