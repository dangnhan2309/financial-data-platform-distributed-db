from sqlalchemy import Column, String, Integer, Date
from api.database import Base


class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_id = Column(String(50), primary_key=True)
    name = Column(String(200))
    unit_of_measure = Column(String(50))
    is_active = Column(Integer)


class PackagingSpecification(Base):
    __tablename__ = "packaging_specification"

    packaging_id = Column(String(50), primary_key=True)
    name = Column(String(200))
    unit_of_measure = Column(String(50))
    volume = Column(Integer)
    material = Column(String(100))


class Certification(Base):
    __tablename__ = "certification"

    certification_id = Column(String(50), primary_key=True)
    name = Column(String(200))
    issue_date = Column(Date)
    expiry_date = Column(Date)
    issued_by = Column(String(200))


class QualityAssurance(Base):
    __tablename__ = "quality_assurance"

    quality_assurance_id = Column(String(50), primary_key=True)
    name = Column(String(200))
    description = Column(String(500))


class ProductType(Base):
    __tablename__ = "product_type"

    product_type_id = Column(String(50), primary_key=True)
    name = Column(String(200))


class Factory(Base):
    __tablename__ = "factory"

    factory_id = Column(String(50), primary_key=True)
    name = Column(String(200))
    address = Column(String(500))


class Incoterm(Base):
    __tablename__ = "incoterm"

    incoterm_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    description = Column(String(500))


class CustomerType(Base):
    __tablename__ = "customer_type"

    customer_type_id = Column(String(50), primary_key=True)
    name = Column(String(100))


class ContractType(Base):
    __tablename__ = "contract_type"

    contract_type_id = Column(String(50), primary_key=True)
    name = Column(String(100))


class PaymentTerm(Base):
    __tablename__ = "payment_term"

    payment_term_id = Column(String(50), primary_key=True)
    description = Column(String(500))


class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(String(50), primary_key=True)
    name = Column(String(200))
    role = Column(String(100))
    email = Column(String(200))
    phone = Column(String(50))


class Bank(Base):
    __tablename__ = "bank"

    bank_id = Column(String(50), primary_key=True)
    bank_name = Column(String(200))
    account_name = Column(String(200))
    account_number = Column(String(100))
    swift_code = Column(String(50))
    bank_address = Column(String(500))
    country = Column(String(100))