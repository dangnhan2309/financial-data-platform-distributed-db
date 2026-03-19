from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AloeProcessingBatchCreate(BaseModel):
    processing_batch_id: str
    factory_id: str
    process_start: datetime
    process_end: datetime | None = None
    input_quantity: Decimal
    output_quantity: Decimal | None = Decimal("0")
    waste_quantity: Decimal | None = Decimal("0")
    status: str | None = None


class AloeProcessingBatchResponse(AloeProcessingBatchCreate):
    model_config = ConfigDict(from_attributes=True)


class RawMaterialInspectionCreate(BaseModel):
    inspection_id: str
    harvest_batch_id: str
    brix: Decimal | None = None
    ph: Decimal | None = None
    size_grade: str | None = None
    accepted_quantity: Decimal | None = None
    rejected_quantity: Decimal | None = None


class RawMaterialInspectionResponse(RawMaterialInspectionCreate):
    model_config = ConfigDict(from_attributes=True)


class FermentationLogCreate(BaseModel):
    fermentation_log_id: str
    processing_batch_id: str
    log_time: datetime
    ph_value: Decimal | None = None
    brix: Decimal | None = None
    temperature_celsius: Decimal | None = None
    note: str | None = None


class FermentationLogResponse(FermentationLogCreate):
    model_config = ConfigDict(from_attributes=True)


class InventoryCreate(BaseModel):
    inventory_id: str
    harvest_batch_id: str | None = None
    production_lot_id: str | None = None
    warehouse_id: str
    quantity: Decimal | None = None
    last_update: datetime | None = None


class InventoryResponse(InventoryCreate):
    model_config = ConfigDict(from_attributes=True)


class QualityTestResultCreate(BaseModel):
    result_id: str
    quality_test_id: str
    test_item_id: str
    actual_value: Decimal | None = None


class QualityTestResultResponse(QualityTestResultCreate):
    model_config = ConfigDict(from_attributes=True)
