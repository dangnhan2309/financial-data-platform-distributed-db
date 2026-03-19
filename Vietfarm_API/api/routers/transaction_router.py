from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.repositories.transaction_repository import (
    aloe_processing_batch_repository,
    fermentation_log_repository,
    inventory_repository,
    quality_test_result_repository,
    raw_material_inspection_repository,
)
from api.schemas.transaction_data import (
    AloeProcessingBatchCreate,
    AloeProcessingBatchResponse,
    FermentationLogCreate,
    FermentationLogResponse,
    InventoryCreate,
    InventoryResponse,
    QualityTestResultCreate,
    QualityTestResultResponse,
    RawMaterialInspectionCreate,
    RawMaterialInspectionResponse,
)
from api.services.transaction_service import create_transaction

router = APIRouter(prefix="/transactions", tags=["Transaction Create APIs"])


@router.post("/aloe-processing-batches", response_model=AloeProcessingBatchResponse, status_code=status.HTTP_201_CREATED)
def create_aloe_processing_batch(payload: AloeProcessingBatchCreate, db: Session = Depends(get_db)):
    return create_transaction(
        aloe_processing_batch_repository,
        db,
        payload.model_dump(),
        "aloe processing batch",
    )


@router.post("/raw-material-inspections", response_model=RawMaterialInspectionResponse, status_code=status.HTTP_201_CREATED)
def create_raw_material_inspection(payload: RawMaterialInspectionCreate, db: Session = Depends(get_db)):
    return create_transaction(
        raw_material_inspection_repository,
        db,
        payload.model_dump(),
        "raw material inspection",
    )


@router.post("/fermentation-logs", response_model=FermentationLogResponse, status_code=status.HTTP_201_CREATED)
def create_fermentation_log(payload: FermentationLogCreate, db: Session = Depends(get_db)):
    return create_transaction(
        fermentation_log_repository,
        db,
        payload.model_dump(),
        "fermentation log",
    )


@router.post("/inventories", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    return create_transaction(
        inventory_repository,
        db,
        payload.model_dump(),
        "inventory",
    )


@router.post("/quality-test-results", response_model=QualityTestResultResponse, status_code=status.HTTP_201_CREATED)
def create_quality_test_result(payload: QualityTestResultCreate, db: Session = Depends(get_db)):
    return create_transaction(
        quality_test_result_repository,
        db,
        payload.model_dump(),
        "quality test result",
    )
