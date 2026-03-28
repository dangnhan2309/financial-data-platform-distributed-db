from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal

from api.models.production_models import (
    AloeProductionLot,
    DispatchOrder,
    DispatchVehicle,
    Inventory,
    PackagingBatch,
)
from generator.config import SeedConfig
from generator.factories.common import add_days, make_id


@dataclass
class ProductionEntities:
    production_lots: list[AloeProductionLot]
    packaging_batches: list[PackagingBatch]
    inventories: list[Inventory]
    dispatch_orders: list[DispatchOrder]
    dispatch_vehicles: list[DispatchVehicle]


def build_production_entities(
    config: SeedConfig,
    processing_batch_ids: list[str],
    packaging_line_ids: list[str],
    warehouse_ids: list[str],
    harvest_batch_ids: list[str],
    vehicle_ids: list[str],
) -> ProductionEntities:
    production_lots: list[AloeProductionLot] = []
    packaging_batches: list[PackagingBatch] = []
    inventories: list[Inventory] = []
    dispatch_orders: list[DispatchOrder] = []
    dispatch_vehicles: list[DispatchVehicle] = []

    packaging_base = datetime(2026, 3, 1, 9, 0, 0)
    dispatch_base = datetime(2026, 3, 5, 8, 0, 0)

    for i in range(1, config.rows_per_table + 1):
        production_lot_id = make_id(config.run_tag, "LOT", i)
        dispatch_id = make_id(config.run_tag, "DSP", i)

        production_lots.append(
            AloeProductionLot(
                production_lot_id=production_lot_id,
                processing_batch_id=processing_batch_ids[(
                    i - 1) % len(processing_batch_ids)],
                product_id=make_id(config.run_tag, "PRD", i),
                production_date=add_days(date(2026, 3, 1), i),
                expiry_date=add_days(date(2026, 6, 1), i),
                quantity=Decimal("800") + Decimal((i - 1) * 2),
                status=["Active", "Hold", "Released"][(i - 1) % 3],
            )
        )

        packaging_batches.append(
            PackagingBatch(
                packaging_batch_id=make_id(config.run_tag, "PKG", i),
                production_lot_id=production_lot_id,
                line_id=packaging_line_ids[(i - 1) % len(packaging_line_ids)],
                packaging_date=packaging_base + timedelta(days=i),
                packaged_quantity=Decimal("700") + Decimal((i - 1) * 2),
            )
        )

        inventories.append(
            Inventory(
                inventory_id=make_id(config.run_tag, "INV", i),
                harvest_batch_id=harvest_batch_ids[(
                    i - 1) % len(harvest_batch_ids)] if i % 2 == 0 else None,
                production_lot_id=production_lot_id if i % 2 == 1 else None,
                warehouse_id=warehouse_ids[(i - 1) % len(warehouse_ids)],
                quantity=Decimal("200") + Decimal((i - 1) * 3),
                last_update=packaging_base + timedelta(days=i, hours=3),
            )
        )

        dispatch_orders.append(
            DispatchOrder(
                dispatch_id=dispatch_id,
                production_lot_id=production_lot_id,
                dispatch_date=dispatch_base + timedelta(days=i),
                destination=f"Customer Location {((i - 1) % 20) + 1}",
            )
        )

        dispatch_vehicles.append(
            DispatchVehicle(
                dispatch_id=dispatch_id,
                vehicle_id=vehicle_ids[(i - 1) % len(vehicle_ids)],
            )
        )

    return ProductionEntities(
        production_lots=production_lots,
        packaging_batches=packaging_batches,
        inventories=inventories,
        dispatch_orders=dispatch_orders,
        dispatch_vehicles=dispatch_vehicles,
    )
