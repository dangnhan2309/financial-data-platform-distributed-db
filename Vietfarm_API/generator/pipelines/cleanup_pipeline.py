from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from api.models.farming_models import (
    AloeField,
    AloeHarvestBatch,
    AloePlantingBatch,
    RawMaterialInspection,
    RawMaterialReceiving,
)
from api.models.master_data_models import (
    AloeFarm,
    Factory,
    Machine,
    Operator,
    PackagingLine,
    QualityTestItem,
    StepType,
    TransportVehicle,
    Warehouse,
)
from api.models.processing_models import (
    AloeProcessingBatch,
    FermentationLog,
    MachineMaintenance,
    ProcessingMaterialUsage,
    ProcessingOperator,
    ProcessingStep,
)
from api.models.production_models import (
    AloeProductionLot,
    DispatchOrder,
    DispatchVehicle,
    Inventory,
    PackagingBatch,
)
from api.models.quality_models import AloeQualityTest, QualityTestResult
from generator.db import get_session, has_table


@dataclass
class CleanupSummary:
    run_tag: str
    deleted_tables: dict[str, int]


def _delete_by_prefix(db: Session, model: type, column_name: str, id_prefix: str) -> int:
    column = getattr(model, column_name)
    return db.query(model).filter(column.like(f"{id_prefix}%")).delete(synchronize_session=False)


def run_cleanup_pipeline(run_tag: str) -> CleanupSummary:
    if not run_tag:
        raise ValueError("run_tag must not be empty")

    id_prefix = f"G{run_tag}_"
    deleted: dict[str, int] = {}

    with get_session() as db:
        try:
            deleted["dispatchvehicle"] = _delete_by_prefix(
                db, DispatchVehicle, "dispatch_id", id_prefix)
            deleted["dispatchorder"] = _delete_by_prefix(
                db, DispatchOrder, "dispatch_id", id_prefix)
            deleted["packagingbatch"] = _delete_by_prefix(
                db, PackagingBatch, "packaging_batch_id", id_prefix)
            deleted["inventory"] = _delete_by_prefix(
                db, Inventory, "inventory_id", id_prefix)

            deleted["qualitytestresult"] = _delete_by_prefix(
                db, QualityTestResult, "result_id", id_prefix)
            deleted["aloequalitytest"] = _delete_by_prefix(
                db, AloeQualityTest, "quality_test_id", id_prefix)

            if has_table("fermentationlog"):
                deleted["fermentationlog"] = _delete_by_prefix(
                    db, FermentationLog, "fermentation_log_id", id_prefix)

            deleted["processingoperator"] = _delete_by_prefix(
                db, ProcessingOperator, "processing_batch_id", id_prefix)
            deleted["processingstep"] = _delete_by_prefix(
                db, ProcessingStep, "step_id", id_prefix)
            deleted["processingmaterialusage"] = _delete_by_prefix(
                db, ProcessingMaterialUsage, "usage_id", id_prefix)
            deleted["machinemaintenance"] = _delete_by_prefix(
                db, MachineMaintenance, "maintenance_id", id_prefix)
            deleted["aloeproductionlot"] = _delete_by_prefix(
                db, AloeProductionLot, "production_lot_id", id_prefix)
            deleted["aloeprocessingbatch"] = _delete_by_prefix(
                db, AloeProcessingBatch, "processing_batch_id", id_prefix)

            deleted["rawmaterialinspection"] = _delete_by_prefix(
                db, RawMaterialInspection, "inspection_id", id_prefix)
            deleted["rawmaterialreceiving"] = _delete_by_prefix(
                db, RawMaterialReceiving, "receiving_id", id_prefix)
            deleted["aloeharvestbatch"] = _delete_by_prefix(
                db, AloeHarvestBatch, "harvest_batch_id", id_prefix)
            deleted["aloeplantingbatch"] = _delete_by_prefix(
                db, AloePlantingBatch, "planting_batch_id", id_prefix)
            deleted["aloefield"] = _delete_by_prefix(
                db, AloeField, "field_id", id_prefix)

            deleted["transportvehicle"] = _delete_by_prefix(
                db, TransportVehicle, "vehicle_id", id_prefix)
            deleted["packagingline"] = _delete_by_prefix(
                db, PackagingLine, "line_id", id_prefix)
            deleted["qualitytestitem"] = _delete_by_prefix(
                db, QualityTestItem, "test_item_id", id_prefix)
            deleted["operator"] = _delete_by_prefix(
                db, Operator, "operator_id", id_prefix)
            deleted["machine"] = _delete_by_prefix(
                db, Machine, "machine_id", id_prefix)
            deleted["steptype"] = _delete_by_prefix(
                db, StepType, "step_type_id", id_prefix)
            deleted["factory"] = _delete_by_prefix(
                db, Factory, "factory_id", id_prefix)
            deleted["warehouse"] = _delete_by_prefix(
                db, Warehouse, "warehouse_id", id_prefix)
            deleted["aloefarm"] = _delete_by_prefix(
                db, AloeFarm, "farm_id", id_prefix)

            db.commit()
            return CleanupSummary(run_tag=run_tag, deleted_tables=deleted)
        except Exception:
            db.rollback()
            raise
