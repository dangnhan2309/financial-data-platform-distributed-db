from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from api.utils.database import Base


class AloeField(Base):
    __tablename__ = "aloefield"

    field_id = Column("field_id", String(50), primary_key=True)
    farm_id = Column("farm_id", String(50), ForeignKey(
        "aloefarm.farm_id"), nullable=False)
    area_hectare = Column("area_hectare", Numeric(10, 2))
    soil_type = Column("soil_type", String(100))
    planting_date = Column("planting_date", Date)
    status = Column("status", String(50))

    farm = relationship("AloeFarm", back_populates="fields")
    planting_batches = relationship(
        "AloePlantingBatch", back_populates="field")


class AloePlantingBatch(Base):
    __tablename__ = "aloeplantingbatch"

    planting_batch_id = Column(
        "planting_batch_id", String(50), primary_key=True)
    field_id = Column("field_id", String(50), ForeignKey(
        "aloefield.field_id"), nullable=False)
    seed_source = Column("seed_source", String(100))
    planting_date = Column("planting_date", Date, nullable=False)
    expected_harvest = Column("expected_harvest", Date)

    field = relationship("AloeField", back_populates="planting_batches")
    harvest_batches = relationship(
        "AloeHarvestBatch", back_populates="planting_batch")


class AloeHarvestBatch(Base):
    __tablename__ = "aloeharvestbatch"

    harvest_batch_id = Column("harvest_batch_id", String(50), primary_key=True)
    farm_id = Column("farm_id", String(50), ForeignKey(
        "aloefarm.farm_id"), nullable=False)
    planting_batch_id = Column(
        "planting_batch_id", String(50), ForeignKey("aloeplantingbatch.planting_batch_id"), nullable=False
    )
    harvest_date = Column("harvest_date", Date, nullable=False)
    quantity_kg = Column("quantity_kg", Numeric(15, 2))
    grade = Column("grade", String(50))

    farm = relationship("AloeFarm", back_populates="harvest_batches")
    planting_batch = relationship(
        "AloePlantingBatch", back_populates="harvest_batches")
    raw_receivings = relationship(
        "RawMaterialReceiving", back_populates="harvest_batch")
    inspections = relationship(
        "RawMaterialInspection", back_populates="harvest_batch")
    material_usages = relationship(
        "ProcessingMaterialUsage", back_populates="harvest_batch")
    inventories = relationship("Inventory", back_populates="harvest_batch")


class RawMaterialReceiving(Base):
    __tablename__ = "rawmaterialreceiving"

    receiving_id = Column("receiving_id", String(50), primary_key=True)
    harvest_batch_id = Column(
        "harvest_batch_id", String(50), ForeignKey("aloeharvestbatch.harvest_batch_id"), nullable=False
    )
    receiving_date = Column("receiving_date", DateTime, nullable=False)
    received_quantity = Column(
        "received_quantity", Numeric(15, 2), nullable=False)
    warehouse_id = Column("warehouse_id", String(50), ForeignKey(
        "warehouse.warehouse_id"), nullable=False)

    harvest_batch = relationship(
        "AloeHarvestBatch", back_populates="raw_receivings")
    warehouse = relationship("Warehouse", back_populates="raw_receivings")


class RawMaterialInspection(Base):
    __tablename__ = "rawmaterialinspection"

    inspection_id = Column("inspection_id", String(50), primary_key=True)
    harvest_batch_id = Column(
        "harvest_batch_id", String(50), ForeignKey("aloeharvestbatch.harvest_batch_id"), nullable=False
    )
    brix = Column("brix", Numeric(5, 2))
    ph = Column("ph", Numeric(4, 2))
    size_grade = Column("size_grade", String(50))
    accepted_quantity = Column("accepted_quantity", Numeric(15, 2))
    rejected_quantity = Column("rejected_quantity", Numeric(15, 2))

    harvest_batch = relationship(
        "AloeHarvestBatch", back_populates="inspections")
