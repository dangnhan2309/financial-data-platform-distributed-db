from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal

from api.models.farming_models import (
    AloeField,
    AloeHarvestBatch,
    AloePlantingBatch,
    RawMaterialInspection,
    RawMaterialReceiving,
)
from generator.config import SeedConfig
from generator.factories.common import add_days, make_id


@dataclass
class FarmingEntities:
    fields: list[AloeField]
    planting_batches: list[AloePlantingBatch]
    harvest_batches: list[AloeHarvestBatch]
    raw_material_receivings: list[RawMaterialReceiving]
    raw_material_inspections: list[RawMaterialInspection]


@dataclass
class FarmingRefs:
    harvest_batch_ids: list[str]


def build_farming_entities(config: SeedConfig, farm_ids: list[str], warehouse_ids: list[str]) -> tuple[FarmingEntities, FarmingRefs]:
    fields: list[AloeField] = []
    planting_batches: list[AloePlantingBatch] = []
    harvest_batches: list[AloeHarvestBatch] = []
    receivings: list[RawMaterialReceiving] = []
    inspections: list[RawMaterialInspection] = []

    base_receiving = datetime(2026, 1, 1, 8, 0, 0)

    for i in range(1, config.rows_per_table + 1):
        field_id = make_id(config.run_tag, "FLD", i)
        planting_id = make_id(config.run_tag, "PLT", i)
        harvest_id = make_id(config.run_tag, "HAR", i)

        farm_id = farm_ids[(i - 1) % len(farm_ids)]
        planting_date = add_days(date(2025, 1, 1), i)

        fields.append(
            AloeField(
                field_id=field_id,
                farm_id=farm_id,
                area_hectare=Decimal("1") + Decimal((i - 1) % 10),
                soil_type=["Sandy Loam", "Loam", "Clay Loam"][(i - 1) % 3],
                planting_date=planting_date,
                status=["Active", "Fallow", "Pre-harvest"][(i - 1) % 3],
            )
        )

        planting_batches.append(
            AloePlantingBatch(
                planting_batch_id=planting_id,
                field_id=field_id,
                seed_source=["Domestic", "Imported", "Hybrid"][(i - 1) % 3],
                planting_date=planting_date,
                expected_harvest=add_days(planting_date, 90),
            )
        )

        harvest_batches.append(
            AloeHarvestBatch(
                harvest_batch_id=harvest_id,
                farm_id=farm_id,
                planting_batch_id=planting_id,
                harvest_date=add_days(planting_date, 95),
                quantity_kg=Decimal("500") + Decimal((i - 1) * 3),
                grade=["A", "B", "C"][(i - 1) % 3],
            )
        )

        receivings.append(
            RawMaterialReceiving(
                receiving_id=make_id(config.run_tag, "RCV", i),
                harvest_batch_id=harvest_id,
                receiving_date=base_receiving + timedelta(days=i),
                received_quantity=Decimal("450") + Decimal((i - 1) * 2),
                warehouse_id=warehouse_ids[(i - 1) % len(warehouse_ids)],
            )
        )

        inspections.append(
            RawMaterialInspection(
                inspection_id=make_id(config.run_tag, "RMI", i),
                harvest_batch_id=harvest_id,
                brix=Decimal("10") + Decimal((i - 1) % 5),
                ph=Decimal("3") + (Decimal((i - 1) % 5) / Decimal("10")),
                size_grade=["S", "M", "L"][(i - 1) % 3],
                accepted_quantity=Decimal("400") + Decimal((i - 1) * 2),
                rejected_quantity=Decimal("20") + Decimal((i - 1) % 10),
            )
        )

    entities = FarmingEntities(
        fields=fields,
        planting_batches=planting_batches,
        harvest_batches=harvest_batches,
        raw_material_receivings=receivings,
        raw_material_inspections=inspections,
    )
    refs = FarmingRefs(harvest_batch_ids=[
                       x.harvest_batch_id for x in harvest_batches])
    return entities, refs
