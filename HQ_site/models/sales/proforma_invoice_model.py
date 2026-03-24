class ProformaInvoice(Base):
    __tablename__ = "proforma_invoice"
    proforma_invoice_id = Column(String(50), primary_key=True)
    quotation_id = Column(String(50), ForeignKey("quotation.quotation_id"))
    payment_term_id = Column(String(50), ForeignKey("payment_term.payment_term_id"))
    bank_id = Column(String(50), ForeignKey("bank.bank_id")) # Bank nằm ở TS_FINANCE
    staff_id = Column(String(50), ForeignKey("staff.staff_id"))
    total_contract_value = Column(Float)
    currency = Column(String(10))
    port_of_loading = Column(String(255))
    port_of_discharge = Column(String(255))
    delivery_time = Column(String(100))
    status = Column(String(20))
    file_path = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())