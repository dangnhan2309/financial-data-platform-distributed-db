from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

# ===== MASTER TABLES =====

class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_id = Column(String, primary_key=True)
    name = Column(String)
    unit_of_measure = Column(String)
    is_active = Column(Integer())


class PackagingSpecification(Base):
    __tablename__ = "packaging_specification"

    packaging_id = Column(String, primary_key=True)
    name = Column(String)
    unit_of_measure = Column(String)
    volume = Column(Integer)
    material = Column(String)


class Certification(Base):
    __tablename__ = "certification"

    certification_id = Column(String, primary_key=True)
    name = Column(String)
    issue_date = Column(Date)
    expiry_date = Column(Date)
    issued_by = Column(String)


class QualityAssurance(Base):
    __tablename__ = "quality_assurance"

    quality_assurance_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)


class ProductType(Base):
    __tablename__ = "product_type"

    product_type_id = Column(String, primary_key=True)
    name = Column(String)


class Factory(Base):
    __tablename__ = "factory"

    factory_id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)


class Incoterm(Base):
    __tablename__ = "incoterm"

    incoterm_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)


class CustomerType(Base):
    __tablename__ = "customer_type"

    customer_type_id = Column(String, primary_key=True)
    name = Column(String)


class ContractType(Base):
    __tablename__ = "contract_type"

    contract_type_id = Column(String, primary_key=True)
    name = Column(String)


class PaymentTerm(Base):
    __tablename__ = "payment_term"

    payment_term_id = Column(String, primary_key=True)
    description = Column(String)


class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String)
    email = Column(String)
    phone = Column(String)


class Bank(Base):
    __tablename__ = "bank"

    bank_id = Column(String, primary_key=True)
    bank_name = Column(String)
    account_name = Column(String)
    account_number = Column(String)
    swift_code = Column(String)
    bank_address = Column(String)
    country = Column(String)


# ===== RELATION TABLES =====

class IngredientProductDetail(Base):
    __tablename__ = "ingredient_product_detail"

    ingredient_id = Column(String, ForeignKey("ingredient.ingredient_id"), primary_key=True)
    product_id = Column(String, ForeignKey("product.product_id"), primary_key=True)
    quantity = Column(Integer)
    unit_of_measure = Column(String)


class ProductSpecification(Base):
    __tablename__ = "product_specification"

    product_specification_id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("product.product_id"))
    packaging_id = Column(String, ForeignKey("packaging_specification.packaging_id"))
    certification_id = Column(String, ForeignKey("certification.certification_id"))
    quality_assurance_id = Column(String, ForeignKey("quality_assurance.quality_assurance_id"))
    shelf_life_days = Column(Integer)
    storage_condition = Column(String)
    origin = Column(String)


class ProductionLot(Base):
    __tablename__ = "production_lot"

    production_lot_id = Column(String, primary_key=True)
    factory_id = Column(String, ForeignKey("factory.factory_id"))
    product_id = Column(String, ForeignKey("product.product_id"))
    production_date = Column(Date)
    expiry_date = Column(Date)
    status = Column(Integer())


class CertificateOfAnalysis(Base):
    __tablename__ = "certificate_of_analysis"

    certificate_of_analysis_id = Column(String, primary_key=True)
    lot_id = Column(String, ForeignKey("production_lot.production_lot_id"))
    issue_date = Column(Date)
