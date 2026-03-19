from sqlalchemy import Boolean, Column, Date, Numeric, String
from sqlalchemy.orm import relationship

from api.utils.database import Base


class AloeFarm(Base):
    __tablename__ = "aloefarm"

    farm_id = Column("farm_id", String(50), primary_key=True)
    farm_name = Column("farm_name", String(100), unique=True, nullable=False)
    farmer_name = Column("farmer_name", String(100))
    location = Column("location", String(255))
    province = Column("province", String(100))
    area_hectare = Column("area_hectare", Numeric(10, 2))
    certification = Column("certification", String(100))
    status = Column("status", Boolean)

    fields = relationship("AloeField", back_populates="farm")
    harvest_batches = relationship("AloeHarvestBatch", back_populates="farm")


class Warehouse(Base):
    __tablename__ = "warehouse"

    warehouse_id = Column("warehouse_id", String(50), primary_key=True)
    warehouse_name = Column("warehouse_name", String(100), nullable=False)
    location = Column("location", String(255))

    raw_receivings = relationship(
        "RawMaterialReceiving", back_populates="warehouse")
    inventories = relationship("Inventory", back_populates="warehouse")


class Factory(Base):
    __tablename__ = "factory"

    factory_id = Column("factory_id", String(50), primary_key=True)
    name = Column("name", String(100), nullable=False)
    address = Column("address", String(255))
    country = Column("country", String(100))

    processing_batches = relationship(
        "AloeProcessingBatch", back_populates="factory")


class StepType(Base):
    __tablename__ = "steptype"

    step_type_id = Column("step_type_id", String(50), primary_key=True)
    step_name = Column("step_name", String(100), nullable=False)

    processing_steps = relationship(
        "ProcessingStep", back_populates="step_type")


class Machine(Base):
    __tablename__ = "machine"

    machine_id = Column("machine_id", String(50), primary_key=True)
    machine_name = Column("machine_name", String(100),
                          unique=True, nullable=False)
    machine_type = Column("machine_type", String(100))
    installation_date = Column("installation_date", Date)
    status = Column("status", String(50))

    maintenances = relationship("MachineMaintenance", back_populates="machine")
    processing_steps = relationship("ProcessingStep", back_populates="machine")


class Operator(Base):
    __tablename__ = "operator"

    operator_id = Column("operator_id", String(50), primary_key=True)
    name = Column("name", String(100), nullable=False)
    role = Column("role", String(100))
    phone = Column("phone", String(20), unique=True)

    processing_operators = relationship(
        "ProcessingOperator", back_populates="operator")


class QualityTestItem(Base):
    __tablename__ = "qualitytestitem"

    test_item_id = Column("test_item_id", String(50), primary_key=True)
    name = Column("name", String(100), nullable=False)
    unit = Column("unit", String(50))
    standard_value = Column("standard_value", Numeric(10, 2))

    quality_test_results = relationship(
        "QualityTestResult", back_populates="test_item")


class PackagingLine(Base):
    __tablename__ = "packagingline"

    line_id = Column("line_id", String(50), primary_key=True)
    line_name = Column("line_name", String(100), nullable=False)
    capacity_per_hour = Column("capacity_per_hour", Numeric(10, 2))

    packaging_batches = relationship("PackagingBatch", back_populates="line")


class TransportVehicle(Base):
    __tablename__ = "transportvehicle"

    vehicle_id = Column("vehicle_id", String(50), primary_key=True)
    license_plate = Column("license_plate", String(50),
                           unique=True, nullable=False)
    capacity = Column("capacity", Numeric(10, 2))

    dispatch_vehicles = relationship(
        "DispatchVehicle", back_populates="vehicle")
