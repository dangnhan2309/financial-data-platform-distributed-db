from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from api.utils.database import Base


class AloeProcessingBatch(Base):
    __tablename__ = "aloeprocessingbatch"

    processing_batch_id = Column(
        "processing_batch_id", String(50), primary_key=True)
    factory_id = Column("factory_id", String(50), ForeignKey(
        "factory.factory_id"), nullable=False)
    process_start = Column("process_start", DateTime, nullable=False)
    process_end = Column("process_end", DateTime)
    input_quantity = Column("input_quantity", Numeric(15, 2), nullable=False)
    output_quantity = Column("output_quantity", Numeric(15, 2), default=0)
    waste_quantity = Column("waste_quantity", Numeric(15, 2), default=0)
    status = Column("status", String(50))

    factory = relationship("Factory", back_populates="processing_batches")
    material_usages = relationship(
        "ProcessingMaterialUsage", back_populates="processing_batch")
    processing_steps = relationship(
        "ProcessingStep", back_populates="processing_batch")
    processing_operators = relationship(
        "ProcessingOperator", back_populates="processing_batch")
    quality_tests = relationship(
        "AloeQualityTest", back_populates="processing_batch")
    production_lots = relationship(
        "AloeProductionLot", back_populates="processing_batch")
    fermentation_logs = relationship(
        "FermentationLog", back_populates="processing_batch")


class MachineMaintenance(Base):
    __tablename__ = "machinemaintenance"

    maintenance_id = Column("maintenance_id", String(50), primary_key=True)
    machine_id = Column("machine_id", String(50), ForeignKey(
        "machine.machine_id"), nullable=False)
    maintenance_date = Column("maintenance_date", Date, nullable=False)
    maintenance_type = Column("maintenance_type", String(100))
    technician = Column("technician", String(100))

    machine = relationship("Machine", back_populates="maintenances")


class ProcessingMaterialUsage(Base):
    __tablename__ = "processingmaterialusage"

    usage_id = Column("usage_id", String(50), primary_key=True)
    processing_batch_id = Column(
        "processing_batch_id", String(50), ForeignKey("aloeprocessingbatch.processing_batch_id"), nullable=False
    )
    harvest_batch_id = Column(
        "harvest_batch_id", String(50), ForeignKey("aloeharvestbatch.harvest_batch_id"), nullable=False
    )
    quantity_used_kg = Column("quantity_used_kg", Numeric(15, 2))

    processing_batch = relationship(
        "AloeProcessingBatch", back_populates="material_usages")
    harvest_batch = relationship(
        "AloeHarvestBatch", back_populates="material_usages")


class ProcessingStep(Base):
    __tablename__ = "processingstep"

    step_id = Column("step_id", String(50), primary_key=True)
    processing_batch_id = Column(
        "processing_batch_id", String(50), ForeignKey("aloeprocessingbatch.processing_batch_id"), nullable=False
    )
    step_type_id = Column("step_type_id", String(
        50), ForeignKey("steptype.step_type_id"), nullable=False)
    machine_id = Column("machine_id", String(50), ForeignKey(
        "machine.machine_id"), nullable=False)
    start_time = Column("start_time", DateTime)
    end_time = Column("end_time", DateTime)

    processing_batch = relationship(
        "AloeProcessingBatch", back_populates="processing_steps")
    step_type = relationship("StepType", back_populates="processing_steps")
    machine = relationship("Machine", back_populates="processing_steps")


class ProcessingOperator(Base):
    __tablename__ = "processingoperator"

    processing_batch_id = Column(
        "processing_batch_id", String(50), ForeignKey("aloeprocessingbatch.processing_batch_id"), primary_key=True
    )
    operator_id = Column("operator_id", String(50), ForeignKey(
        "operator.operator_id"), primary_key=True)

    processing_batch = relationship(
        "AloeProcessingBatch", back_populates="processing_operators")
    operator = relationship("Operator", back_populates="processing_operators")


class FermentationLog(Base):
    __tablename__ = "fermentationlog"

    fermentation_log_id = Column(
        "fermentation_log_id", String(50), primary_key=True)
    processing_batch_id = Column(
        "processing_batch_id", String(50), ForeignKey("aloeprocessingbatch.processing_batch_id"), nullable=False
    )
    log_time = Column("log_time", DateTime, nullable=False)
    ph_value = Column("ph_value", Numeric(5, 2))
    brix = Column("brix", Numeric(5, 2))
    temperature_celsius = Column("temperature_celsius", Numeric(5, 2))
    note = Column("note", String(255))

    processing_batch = relationship(
        "AloeProcessingBatch", back_populates="fermentation_logs")
