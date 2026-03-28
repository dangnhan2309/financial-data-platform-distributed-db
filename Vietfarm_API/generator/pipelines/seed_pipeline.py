from __future__ import annotations

from dataclasses import dataclass

from generator.config import SeedConfig
from generator.db import bulk_insert, get_session, has_table
from generator.factories import (
    build_farming_entities,
    build_master_data_entities,
    build_processing_entities,
    build_production_entities,
    build_quality_entities,
)
from generator.validators import ensure_required_tables


@dataclass
class SeedSummary:
    rows_per_table: int
    run_tag: str
    inserted_tables: dict[str, int]
    fermentation_enabled: bool


def run_seed_pipeline(config: SeedConfig) -> SeedSummary:
    ensure_required_tables()
    fermentation_enabled = has_table("fermentationlog")

    with get_session() as db:
        try:
            inserted: dict[str, int] = {}

            master_entities, master_refs = build_master_data_entities(config)
            bulk_insert(db, master_entities.farms)
            bulk_insert(db, master_entities.warehouses)
            bulk_insert(db, master_entities.factories)
            bulk_insert(db, master_entities.step_types)
            bulk_insert(db, master_entities.machines)
            bulk_insert(db, master_entities.operators)
            bulk_insert(db, master_entities.quality_test_items)
            bulk_insert(db, master_entities.packaging_lines)
            bulk_insert(db, master_entities.vehicles)
            db.commit()
            inserted.update(
                {
                    "aloefarm": len(master_entities.farms),
                    "warehouse": len(master_entities.warehouses),
                    "factory": len(master_entities.factories),
                    "steptype": len(master_entities.step_types),
                    "machine": len(master_entities.machines),
                    "operator": len(master_entities.operators),
                    "qualitytestitem": len(master_entities.quality_test_items),
                    "packagingline": len(master_entities.packaging_lines),
                    "transportvehicle": len(master_entities.vehicles),
                }
            )

            farming_entities, farming_refs = build_farming_entities(
                config,
                farm_ids=master_refs.farm_ids,
                warehouse_ids=master_refs.warehouse_ids,
            )
            bulk_insert(db, farming_entities.fields)
            bulk_insert(db, farming_entities.planting_batches)
            bulk_insert(db, farming_entities.harvest_batches)
            bulk_insert(db, farming_entities.raw_material_receivings)
            bulk_insert(db, farming_entities.raw_material_inspections)
            db.commit()
            inserted.update(
                {
                    "aloefield": len(farming_entities.fields),
                    "aloeplantingbatch": len(farming_entities.planting_batches),
                    "aloeharvestbatch": len(farming_entities.harvest_batches),
                    "rawmaterialreceiving": len(farming_entities.raw_material_receivings),
                    "rawmaterialinspection": len(farming_entities.raw_material_inspections),
                }
            )

            processing_entities, processing_refs = build_processing_entities(
                config,
                factory_ids=master_refs.factory_ids,
                machine_ids=master_refs.machine_ids,
                operator_ids=master_refs.operator_ids,
                step_type_ids=master_refs.step_type_ids,
                harvest_batch_ids=farming_refs.harvest_batch_ids,
            )
            bulk_insert(db, processing_entities.processing_batches)
            bulk_insert(db, processing_entities.material_usages)
            bulk_insert(db, processing_entities.processing_steps)
            bulk_insert(db, processing_entities.processing_operators)
            bulk_insert(db, processing_entities.machine_maintenances)
            if fermentation_enabled:
                bulk_insert(db, processing_entities.fermentation_logs)
            db.commit()
            inserted.update(
                {
                    "aloeprocessingbatch": len(processing_entities.processing_batches),
                    "processingmaterialusage": len(processing_entities.material_usages),
                    "processingstep": len(processing_entities.processing_steps),
                    "processingoperator": len(processing_entities.processing_operators),
                    "machinemaintenance": len(processing_entities.machine_maintenances),
                }
            )
            if fermentation_enabled:
                inserted["fermentationlog"] = len(
                    processing_entities.fermentation_logs)

            quality_entities = build_quality_entities(
                config,
                processing_batch_ids=processing_refs.processing_batch_ids,
                test_item_ids=master_refs.quality_test_item_ids,
            )
            bulk_insert(db, quality_entities.quality_tests)
            bulk_insert(db, quality_entities.quality_test_results)
            db.commit()
            inserted.update(
                {
                    "aloequalitytest": len(quality_entities.quality_tests),
                    "qualitytestresult": len(quality_entities.quality_test_results),
                }
            )

            production_entities = build_production_entities(
                config,
                processing_batch_ids=processing_refs.processing_batch_ids,
                packaging_line_ids=master_refs.packaging_line_ids,
                warehouse_ids=master_refs.warehouse_ids,
                harvest_batch_ids=farming_refs.harvest_batch_ids,
                vehicle_ids=master_refs.vehicle_ids,
            )
            bulk_insert(db, production_entities.production_lots)
            bulk_insert(db, production_entities.packaging_batches)
            bulk_insert(db, production_entities.inventories)
            bulk_insert(db, production_entities.dispatch_orders)
            bulk_insert(db, production_entities.dispatch_vehicles)
            db.commit()
            inserted.update(
                {
                    "aloeproductionlot": len(production_entities.production_lots),
                    "packagingbatch": len(production_entities.packaging_batches),
                    "inventory": len(production_entities.inventories),
                    "dispatchorder": len(production_entities.dispatch_orders),
                    "dispatchvehicle": len(production_entities.dispatch_vehicles),
                }
            )

            return SeedSummary(
                rows_per_table=config.rows_per_table,
                run_tag=config.run_tag,
                inserted_tables=inserted,
                fermentation_enabled=fermentation_enabled,
            )

        except Exception:
            db.rollback()
            raise
