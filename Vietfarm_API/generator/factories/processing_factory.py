from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal

from api.models.processing_models import (
    AloeProcessingBatch,
    FermentationLog,
    MachineMaintenance,
    ProcessingMaterialUsage,
    ProcessingOperator,
    ProcessingStep,
)
from generator.config import SeedConfig
from generator.factories.common import add_days, add_hours, make_id


@dataclass
class ProcessingEntities:
    processing_batches: list[AloeProcessingBatch]
    material_usages: list[ProcessingMaterialUsage]
    processing_steps: list[ProcessingStep]
    processing_operators: list[ProcessingOperator]
    machine_maintenances: list[MachineMaintenance]
    fermentation_logs: list[FermentationLog]


@dataclass
class ProcessingRefs:
    processing_batch_ids: list[str]


def build_processing_entities(
    config: SeedConfig,
    factory_ids: list[str],
    machine_ids: list[str],
    operator_ids: list[str],
    step_type_ids: list[str],
    harvest_batch_ids: list[str],
) -> tuple[ProcessingEntities, ProcessingRefs]:
    processing_batches: list[AloeProcessingBatch] = []
    material_usages: list[ProcessingMaterialUsage] = []
    processing_steps: list[ProcessingStep] = []
    processing_operators: list[ProcessingOperator] = []
    machine_maintenances: list[MachineMaintenance] = []
    fermentation_logs: list[FermentationLog] = []

    base_start = datetime(2026, 2, 1, 6, 0, 0)

    for i in range(1, config.rows_per_table + 1):
        processing_batch_id = make_id(config.run_tag, "PB", i)
        start_time = base_start + timedelta(days=i)
        end_time = add_hours(start_time, 6)

        processing_batches.append(
            AloeProcessingBatch(
                processing_batch_id=processing_batch_id,
                factory_id=factory_ids[(i - 1) % len(factory_ids)],
                process_start=start_time,
                process_end=end_time,
                input_quantity=Decimal("1000") + Decimal((i - 1) * 5),
                output_quantity=Decimal("900") + Decimal((i - 1) * 4),
                waste_quantity=Decimal("100") + Decimal((i - 1)),
                status=["In-Progress", "Completed", "Failed"][(i - 1) % 3],
            )
        )

        material_usages.append(
            ProcessingMaterialUsage(
                usage_id=make_id(config.run_tag, "USE", i),
                processing_batch_id=processing_batch_id,
                harvest_batch_id=harvest_batch_ids[(
                    i - 1) % len(harvest_batch_ids)],
                quantity_used_kg=Decimal("300") + Decimal((i - 1) * 2),
            )
        )

        processing_steps.append(
            ProcessingStep(
                step_id=make_id(config.run_tag, "STEP", i),
                processing_batch_id=processing_batch_id,
                step_type_id=step_type_ids[(i - 1) % len(step_type_ids)],
                machine_id=machine_ids[(i - 1) % len(machine_ids)],
                start_time=start_time,
                end_time=add_hours(start_time, 1),
            )
        )

        processing_operators.append(
            ProcessingOperator(
                processing_batch_id=processing_batch_id,
                operator_id=operator_ids[(i - 1) % len(operator_ids)],
            )
        )

        machine_maintenances.append(
            MachineMaintenance(
                maintenance_id=make_id(config.run_tag, "MNT", i),
                machine_id=machine_ids[(i - 1) % len(machine_ids)],
                maintenance_date=add_days(date(2026, 1, 1), i),
                maintenance_type=["Preventive", "Corrective",
                                  "Calibration"][(i - 1) % 3],
                technician=f"Technician {i}",
            )
        )

        fermentation_logs.append(
            FermentationLog(
                fermentation_log_id=make_id(config.run_tag, "FER", i),
                processing_batch_id=processing_batch_id,
                log_time=add_hours(start_time, 2),
                ph_value=Decimal("3.2") + (Decimal((i - 1) %
                                                   5) / Decimal("10")),
                brix=Decimal("11") + Decimal((i - 1) % 4),
                temperature_celsius=Decimal("25") + Decimal((i - 1) % 6),
                note=f"Fermentation log {i}",
            )
        )

    entities = ProcessingEntities(
        processing_batches=processing_batches,
        material_usages=material_usages,
        processing_steps=processing_steps,
        processing_operators=processing_operators,
        machine_maintenances=machine_maintenances,
        fermentation_logs=fermentation_logs,
    )
    refs = ProcessingRefs(processing_batch_ids=[
                          x.processing_batch_id for x in processing_batches])
    return entities, refs
