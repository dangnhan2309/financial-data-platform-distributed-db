class ContractType(Base):
    __tablename__ = "contract_type"
    contract_type_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    status = Column(String(20))