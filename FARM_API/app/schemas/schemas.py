from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date

# --- Base Models ---

# Farm
class FarmBase(BaseModel):
    farm_id: str
    farm_name: str
    location: Optional[str] = None
    created_at: Optional[datetime] = None

class FarmCreate(FarmBase):
    pass

class Farm(FarmBase):
    class Config:
        from_attributes = True

# Plot
class FarmPlotBase(BaseModel):
    plot_id: str
    farm_id: str
    plot_name: str
    crop_type: Optional[str] = None
    area_m2: Optional[float] = None

class FarmPlotCreate(FarmPlotBase):
    pass

class FarmPlot(FarmPlotBase):
    class Config:
        from_attributes = True

# Bed
class FarmBedBase(BaseModel):
    bed_id: str
    plot_id: str
    bed_number: int
    planting_date: Optional[date] = None
    status: Optional[str] = None

class FarmBedCreate(FarmBedBase):
    pass

class FarmBed(FarmBedBase):
    class Config:
        from_attributes = True

# IoT Sensor
class IotSensorBase(BaseModel):
    sensor_id: str
    plot_id: str
    sensor_type: Optional[str] = None
    manufacturer: Optional[str] = None
    status: Optional[str] = None
    installed_at: Optional[datetime] = None

class IotSensorCreate(IotSensorBase):
    pass

class IotSensor(IotSensorBase):
    class Config:
        from_attributes = True

# Sensor Data
class SensorDataBase(BaseModel):
    data_id: str
    sensor_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    soil_moisture: Optional[float] = None
    light_intensity: Optional[float] = None
    recorded_at: Optional[datetime] = None

class SensorDataCreate(SensorDataBase):
    pass

class SensorData(SensorDataBase):
    class Config:
        from_attributes = True

# Cultivation Log
class CultivationLogBase(BaseModel):
    log_id: str
    bed_id: str
    action: Optional[str] = None
    performed_by: Optional[str] = None
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class CultivationLogCreate(CultivationLogBase):
    pass

class CultivationLog(CultivationLogBase):
    class Config:
        from_attributes = True

# Ingredient
class IngredientBase(BaseModel):
    ingredient_id: str
    name: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    class Config:
        from_attributes = True

# Weighing Ticket
class WeighingTicketBase(BaseModel):
    ticket_id: str
    bed_id: str
    ingredient_id: str
    raw_weight: Optional[float] = None
    harvested_by: Optional[str] = None
    timestamp: Optional[datetime] = None

class WeighingTicketCreate(WeighingTicketBase):
    pass

class WeighingTicket(WeighingTicketBase):
    class Config:
        from_attributes = True

# Supplier
class SupplierBase(BaseModel):
    supplier_id: str
    supplier_name: str
    supplier_type: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    class Config:
        from_attributes = True

# Purchase Contract
class PurchaseContractBase(BaseModel):
    contract_id: str
    supplier_id: str
    ingredient_id: str
    committed_quantity: Optional[float] = None
    contract_price: Optional[float] = None
    quality_commitment: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class PurchaseContractCreate(PurchaseContractBase):
    pass

class PurchaseContract(PurchaseContractBase):
    class Config:
        from_attributes = True

# Purchase Batch
class PurchaseBatchBase(BaseModel):
    batch_id: str
    contract_id: str
    purchase_date: Optional[date] = None
    expected_quantity: Optional[float] = None
    unit_price: Optional[float] = None
    status: Optional[str] = None

class PurchaseBatchCreate(PurchaseBatchBase):
    pass

class PurchaseBatch(PurchaseBatchBase):
    class Config:
        from_attributes = True

# Purchase Ticket
class PurchaseTicketBase(BaseModel):
    ticket_id: str
    batch_id: str
    supplier_id: str
    ingredient_id: str
    raw_weight: Optional[float] = None
    received_at: Optional[datetime] = None

class PurchaseTicketCreate(PurchaseTicketBase):
    pass

class PurchaseTicket(PurchaseTicketBase):
    class Config:
        from_attributes = True

# Production Lot
class ProductionLotBase(BaseModel):
    lot_id: str
    product_id: Optional[str] = None
    mfg_date: Optional[datetime] = None
    exp_date: Optional[datetime] = None

class ProductionLotCreate(ProductionLotBase):
    pass

class ProductionLot(ProductionLotBase):
    class Config:
        from_attributes = True

# --- Warehouse ---
class WarehouseBase(BaseModel):
    warehouse_id: str
    warehouse_name: str
    location: Optional[str] = None
    capacity_ton: Optional[float] = None

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    class Config:
        from_attributes = True

# --- Inventory ---
class InventoryBase(BaseModel):
    inventory_id: str
    warehouse_id: str
    inventory_type: str
    item_id: str
    lot_number: Optional[str] = None
    origin_source: Optional[str] = None
    origin_ref_id: Optional[str] = None
    quantity_kg: float
    updated_at: Optional[datetime] = None

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    class Config:
        from_attributes = True

# --- QC Models ---
class QCReceivingBase(BaseModel):
    qc_id: str
    purchase_ticket_id: str
    inspector_name: Optional[str] = None
    sample_size: Optional[float] = None
    defects_found: Optional[float] = None
    quality_score: Optional[float] = None
    pass_status: Optional[str] = None
    notes: Optional[str] = None
    checked_at: Optional[datetime] = None

class QCReceivingCreate(QCReceivingBase):
    pass

class QCReceiving(QCReceivingBase):
    class Config:
        from_attributes = True

class QCHarvestBase(BaseModel):
    qc_id: str
    weighing_ticket_id: str
    inspector_name: Optional[str] = None
    appearance_grade: Optional[str] = None
    defect_notes: Optional[str] = None
    pass_status: Optional[str] = None
    checked_at: Optional[datetime] = None

class QCHarvestCreate(QCHarvestBase):
    pass

class QCHarvest(QCHarvestBase):
    class Config:
        from_attributes = True

class QCProductLotBase(BaseModel):
    qc_id: str
    production_lot_id: str
    inspector_name: Optional[str] = None
    brix_level: Optional[float] = None
    ph_level: Optional[float] = None
    pesticide_residue_check: Optional[str] = None
    final_grade: Optional[str] = None
    checked_at: Optional[datetime] = None

class QCProductLotCreate(QCProductLotBase):
    pass

class QCProductLot(QCProductLotBase):
    class Config:
        from_attributes = True

# --- B2C Models ---
class CustomerBase(BaseModel):
    customer_id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    loyalty_points: Optional[int] = 0

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    class Config:
        from_attributes = True

class SalesItemBase(BaseModel):
    item_id: str
    order_id: str
    product_id: str
    quantity: float
    unit_price: float
    subtotal: float

class SalesItemCreate(SalesItemBase):
    pass

class SalesItem(SalesItemBase):
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    payment_id: str
    order_id: str
    payment_method: Optional[str] = None
    amount: float
    payment_date: Optional[datetime] = None
    status: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    class Config:
        from_attributes = True

class SalesOrderBase(BaseModel):
    order_id: str
    customer_id: str
    order_date: Optional[datetime] = None
    status: Optional[str] = None
    total_amount: float
    shipping_address: Optional[str] = None

class SalesOrderCreate(SalesOrderBase):
    pass

class SalesOrder(SalesOrderBase):
    items: List[SalesItem] = []
    payments: List[Payment] = []
    
    class Config:
        from_attributes = True

