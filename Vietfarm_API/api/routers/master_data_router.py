from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.repositories.master_data_repository import (
    aloe_farm_repository,
    factory_repository,
    machine_repository,
    quality_test_item_repository,
    step_type_repository,
    warehouse_repository,
)
from api.schemas.master_data import (
    AloeFarmCreate,
    AloeFarmResponse,
    AloeFarmUpdate,
    FactoryCreate,
    FactoryResponse,
    FactoryUpdate,
    MachineCreate,
    MachineResponse,
    MachineUpdate,
    QualityTestItemCreate,
    QualityTestItemResponse,
    QualityTestItemUpdate,
    StepTypeCreate,
    StepTypeResponse,
    StepTypeUpdate,
    WarehouseCreate,
    WarehouseResponse,
    WarehouseUpdate,
)
from api.services.master_data_service import (
    create_entity,
    delete_entity,
    get_entity_or_404,
    list_entities,
    update_entity,
)

router = APIRouter(prefix="/master-data", tags=["Master Data CRUD"])


@router.get("/factories", response_model=list[FactoryResponse])
def list_factories(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_entities(factory_repository, db, offset, limit)


@router.post("/factories", response_model=FactoryResponse, status_code=status.HTTP_201_CREATED)
def create_factory(payload: FactoryCreate, db: Session = Depends(get_db)):
    return create_entity(factory_repository, db, payload.model_dump(), "factory")


@router.get("/factories/{factory_id}", response_model=FactoryResponse)
def get_factory(factory_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(factory_repository, db, factory_id, "Factory")


@router.put("/factories/{factory_id}", response_model=FactoryResponse)
def update_factory(factory_id: str, payload: FactoryUpdate, db: Session = Depends(get_db)):
    entity = get_entity_or_404(factory_repository, db, factory_id, "Factory")
    return update_entity(factory_repository, db, entity, payload.model_dump(), "factory")


@router.delete("/factories/{factory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_factory(factory_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(factory_repository, db, factory_id, "Factory")
    delete_entity(factory_repository, db, entity, "factory")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/warehouses", response_model=list[WarehouseResponse])
def list_warehouses(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_entities(warehouse_repository, db, offset, limit)


@router.post("/warehouses", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(payload: WarehouseCreate, db: Session = Depends(get_db)):
    return create_entity(warehouse_repository, db, payload.model_dump(), "warehouse")


@router.get("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(warehouse_repository, db, warehouse_id, "Warehouse")


@router.put("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(warehouse_id: str, payload: WarehouseUpdate, db: Session = Depends(get_db)):
    entity = get_entity_or_404(
        warehouse_repository, db, warehouse_id, "Warehouse")
    return update_entity(warehouse_repository, db, entity, payload.model_dump(), "warehouse")


@router.delete("/warehouses/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(
        warehouse_repository, db, warehouse_id, "Warehouse")
    delete_entity(warehouse_repository, db, entity, "warehouse")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/aloe-farms", response_model=list[AloeFarmResponse])
def list_aloe_farms(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_entities(aloe_farm_repository, db, offset, limit)


@router.post("/aloe-farms", response_model=AloeFarmResponse, status_code=status.HTTP_201_CREATED)
def create_aloe_farm(payload: AloeFarmCreate, db: Session = Depends(get_db)):
    return create_entity(aloe_farm_repository, db, payload.model_dump(), "aloe farm")


@router.get("/aloe-farms/{farm_id}", response_model=AloeFarmResponse)
def get_aloe_farm(farm_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(aloe_farm_repository, db, farm_id, "AloeFarm")


@router.put("/aloe-farms/{farm_id}", response_model=AloeFarmResponse)
def update_aloe_farm(farm_id: str, payload: AloeFarmUpdate, db: Session = Depends(get_db)):
    entity = get_entity_or_404(aloe_farm_repository, db, farm_id, "AloeFarm")
    return update_entity(aloe_farm_repository, db, entity, payload.model_dump(), "aloe farm")


@router.delete("/aloe-farms/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aloe_farm(farm_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(aloe_farm_repository, db, farm_id, "AloeFarm")
    delete_entity(aloe_farm_repository, db, entity, "aloe farm")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/step-types", response_model=list[StepTypeResponse])
def list_step_types(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_entities(step_type_repository, db, offset, limit)


@router.post("/step-types", response_model=StepTypeResponse, status_code=status.HTTP_201_CREATED)
def create_step_type(payload: StepTypeCreate, db: Session = Depends(get_db)):
    return create_entity(step_type_repository, db, payload.model_dump(), "step type")


@router.get("/step-types/{step_type_id}", response_model=StepTypeResponse)
def get_step_type(step_type_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(step_type_repository, db, step_type_id, "StepType")


@router.put("/step-types/{step_type_id}", response_model=StepTypeResponse)
def update_step_type(step_type_id: str, payload: StepTypeUpdate, db: Session = Depends(get_db)):
    entity = get_entity_or_404(
        step_type_repository, db, step_type_id, "StepType")
    return update_entity(step_type_repository, db, entity, payload.model_dump(), "step type")


@router.delete("/step-types/{step_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_step_type(step_type_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(
        step_type_repository, db, step_type_id, "StepType")
    delete_entity(step_type_repository, db, entity, "step type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/machines", response_model=list[MachineResponse])
def list_machines(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_entities(machine_repository, db, offset, limit)


@router.post("/machines", response_model=MachineResponse, status_code=status.HTTP_201_CREATED)
def create_machine(payload: MachineCreate, db: Session = Depends(get_db)):
    return create_entity(machine_repository, db, payload.model_dump(), "machine")


@router.get("/machines/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(machine_repository, db, machine_id, "Machine")


@router.put("/machines/{machine_id}", response_model=MachineResponse)
def update_machine(machine_id: str, payload: MachineUpdate, db: Session = Depends(get_db)):
    entity = get_entity_or_404(machine_repository, db, machine_id, "Machine")
    return update_entity(machine_repository, db, entity, payload.model_dump(), "machine")


@router.delete("/machines/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(machine_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(machine_repository, db, machine_id, "Machine")
    delete_entity(machine_repository, db, entity, "machine")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/quality-test-items", response_model=list[QualityTestItemResponse])
def list_quality_test_items(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_entities(quality_test_item_repository, db, offset, limit)


@router.post("/quality-test-items", response_model=QualityTestItemResponse, status_code=status.HTTP_201_CREATED)
def create_quality_test_item(payload: QualityTestItemCreate, db: Session = Depends(get_db)):
    return create_entity(quality_test_item_repository, db, payload.model_dump(), "quality test item")


@router.get("/quality-test-items/{test_item_id}", response_model=QualityTestItemResponse)
def get_quality_test_item(test_item_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(quality_test_item_repository, db, test_item_id, "QualityTestItem")


@router.put("/quality-test-items/{test_item_id}", response_model=QualityTestItemResponse)
def update_quality_test_item(test_item_id: str, payload: QualityTestItemUpdate, db: Session = Depends(get_db)):
    entity = get_entity_or_404(
        quality_test_item_repository, db, test_item_id, "QualityTestItem")
    return update_entity(quality_test_item_repository, db, entity, payload.model_dump(), "quality test item")


@router.delete("/quality-test-items/{test_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quality_test_item(test_item_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(
        quality_test_item_repository, db, test_item_id, "QualityTestItem")
    delete_entity(quality_test_item_repository,
                  db, entity, "quality test item")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
