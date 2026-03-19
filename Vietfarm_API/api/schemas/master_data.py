from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AloeFarmBase(BaseModel):
    farm_name: str
    farmer_name: str | None = None
    location: str | None = None
    province: str | None = None
    area_hectare: Decimal | None = None
    certification: str | None = None
    status: bool | None = None


class AloeFarmCreate(AloeFarmBase):
    farm_id: str


class AloeFarmUpdate(AloeFarmBase):
    pass


class AloeFarmResponse(AloeFarmCreate):
    model_config = ConfigDict(from_attributes=True)


class FactoryBase(BaseModel):
    name: str
    address: str | None = None
    country: str | None = None


class FactoryCreate(FactoryBase):
    factory_id: str


class FactoryUpdate(FactoryBase):
    pass


class FactoryResponse(FactoryCreate):
    model_config = ConfigDict(from_attributes=True)


class WarehouseBase(BaseModel):
    warehouse_name: str
    location: str | None = None


class WarehouseCreate(WarehouseBase):
    warehouse_id: str


class WarehouseUpdate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseCreate):
    model_config = ConfigDict(from_attributes=True)


class StepTypeBase(BaseModel):
    step_name: str


class StepTypeCreate(StepTypeBase):
    step_type_id: str


class StepTypeUpdate(StepTypeBase):
    pass


class StepTypeResponse(StepTypeCreate):
    model_config = ConfigDict(from_attributes=True)


class MachineBase(BaseModel):
    machine_name: str
    machine_type: str | None = None
    installation_date: date | None = None
    status: str | None = None


class MachineCreate(MachineBase):
    machine_id: str


class MachineUpdate(MachineBase):
    pass


class MachineResponse(MachineCreate):
    model_config = ConfigDict(from_attributes=True)


class QualityTestItemBase(BaseModel):
    name: str
    unit: str | None = None
    standard_value: Decimal | None = None


class QualityTestItemCreate(QualityTestItemBase):
    test_item_id: str


class QualityTestItemUpdate(QualityTestItemBase):
    pass


class QualityTestItemResponse(QualityTestItemCreate):
    model_config = ConfigDict(from_attributes=True)
