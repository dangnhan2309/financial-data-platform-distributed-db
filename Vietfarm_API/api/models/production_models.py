from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from api.utils.database import Base


class AloeProductionLot(Base):
    __tablename__ = "aloeproductionlot"

    production_lot_id = Column(
        "production_lot_id", String(50), primary_key=True)
    processing_batch_id = Column(
        "processing_batch_id", String(50), ForeignKey("aloeprocessingbatch.processing_batch_id"), nullable=False
    )
    product_id = Column("product_id", String(50))
    production_date = Column("production_date", Date, nullable=False)
    expiry_date = Column("expiry_date", Date)
    quantity = Column("quantity", Numeric(15, 2))
    status = Column("status", String(50))

    processing_batch = relationship(
        "AloeProcessingBatch", back_populates="production_lots")
    packaging_batches = relationship(
        "PackagingBatch", back_populates="production_lot")
    inventories = relationship("Inventory", back_populates="production_lot")
    dispatch_orders = relationship(
        "DispatchOrder", back_populates="production_lot")


class PackagingBatch(Base):
    __tablename__ = "packagingbatch"

    packaging_batch_id = Column(
        "packaging_batch_id", String(50), primary_key=True)
    production_lot_id = Column(
        "production_lot_id", String(50), ForeignKey("aloeproductionlot.production_lot_id"), nullable=False
    )
    line_id = Column("line_id", String(50), ForeignKey(
        "packagingline.line_id"), nullable=False)
    packaging_date = Column("packaging_date", DateTime)
    packaged_quantity = Column("packaged_quantity", Numeric(15, 2))

    production_lot = relationship(
        "AloeProductionLot", back_populates="packaging_batches")
    line = relationship("PackagingLine", back_populates="packaging_batches")


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column("inventory_id", String(50), primary_key=True)
    harvest_batch_id = Column("harvest_batch_id", String(
        50), ForeignKey("aloeharvestbatch.harvest_batch_id"))
    production_lot_id = Column("production_lot_id", String(
        50), ForeignKey("aloeproductionlot.production_lot_id"))
    warehouse_id = Column("warehouse_id", String(50), ForeignKey(
        "warehouse.warehouse_id"), nullable=False)
    quantity = Column("quantity", Numeric(15, 2))
    last_update = Column("last_update", DateTime)

    harvest_batch = relationship(
        "AloeHarvestBatch", back_populates="inventories")
    production_lot = relationship(
        "AloeProductionLot", back_populates="inventories")
    warehouse = relationship("Warehouse", back_populates="inventories")


class DispatchOrder(Base):
    __tablename__ = "dispatchorder"

    dispatch_id = Column("dispatch_id", String(50), primary_key=True)
    production_lot_id = Column(
        "production_lot_id", String(50), ForeignKey("aloeproductionlot.production_lot_id"), nullable=False
    )
    dispatch_date = Column("dispatch_date", DateTime)
    destination = Column("destination", String(255))

    production_lot = relationship(
        "AloeProductionLot", back_populates="dispatch_orders")
    dispatch_vehicles = relationship(
        "DispatchVehicle", back_populates="dispatch")


class DispatchVehicle(Base):
    __tablename__ = "dispatchvehicle"

    dispatch_id = Column("dispatch_id", String(50), ForeignKey(
        "dispatchorder.dispatch_id"), primary_key=True)
    vehicle_id = Column("vehicle_id", String(50), ForeignKey(
        "transportvehicle.vehicle_id"), primary_key=True)

    dispatch = relationship(
        "DispatchOrder", back_populates="dispatch_vehicles")
    vehicle = relationship(
        "TransportVehicle", back_populates="dispatch_vehicles")
