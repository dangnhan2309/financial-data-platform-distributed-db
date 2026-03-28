from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from random import Random

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
from generator.config import SeedConfig
from generator.factories.common import add_days, make_id


@dataclass
class MasterDataEntities:
    farms: list[AloeFarm]
    warehouses: list[Warehouse]
    factories: list[Factory]
    step_types: list[StepType]
    machines: list[Machine]
    operators: list[Operator]
    quality_test_items: list[QualityTestItem]
    packaging_lines: list[PackagingLine]
    vehicles: list[TransportVehicle]


@dataclass
class MasterDataRefs:
    farm_ids: list[str]
    warehouse_ids: list[str]
    factory_ids: list[str]
    step_type_ids: list[str]
    machine_ids: list[str]
    operator_ids: list[str]
    quality_test_item_ids: list[str]
    packaging_line_ids: list[str]
    vehicle_ids: list[str]


def build_master_data_entities(config: SeedConfig) -> tuple[MasterDataEntities, MasterDataRefs]:
    rnd = Random(config.random_seed)
    provinces = ["Ninh Thuan", "Binh Thuan", "Dong Nai", "Lam Dong", "Dak Lak"]
    certs = ["VietGAP", "GlobalGAP", "Organic", "ISO22000"]

    farms: list[AloeFarm] = []
    warehouses: list[Warehouse] = []
    factories: list[Factory] = []
    step_types: list[StepType] = []
    machines: list[Machine] = []
    operators: list[Operator] = []
    quality_test_items: list[QualityTestItem] = []
    packaging_lines: list[PackagingLine] = []
    vehicles: list[TransportVehicle] = []

    for i in range(1, config.rows_per_table + 1):
        farms.append(
            AloeFarm(
                farm_id=make_id(config.run_tag, "FARM", i),
                farm_name=f"VietFarm Aloe Farm {config.run_tag}-{i}",
                farmer_name=f"Farmer {i}",
                location=f"Zone {((i - 1) % 10) + 1}",
                province=provinces[(i - 1) % len(provinces)],
                area_hectare=Decimal("5") + Decimal(i % 20),
                certification=certs[(i - 1) % len(certs)],
                status=True,
            )
        )

        warehouses.append(
            Warehouse(
                warehouse_id=make_id(config.run_tag, "WH", i),
                warehouse_name=f"Warehouse {config.run_tag}-{i}",
                location=f"Factory Area {((i - 1) % 5) + 1}",
            )
        )

        factories.append(
            Factory(
                factory_id=make_id(config.run_tag, "FAC", i),
                name=f"VietFarm Factory {config.run_tag}-{i}",
                address=f"Industrial Park {((i - 1) % 8) + 1}",
                country="Viet Nam",
            )
        )

        step_types.append(
            StepType(
                step_type_id=make_id(config.run_tag, "STP", i),
                step_name=f"Process Step {i}",
            )
        )

        machines.append(
            Machine(
                machine_id=make_id(config.run_tag, "MAC", i),
                machine_name=f"Machine {config.run_tag}-{i}",
                machine_type=["Washing", "Dicing",
                              "Pasteurization", "Mixing"][(i - 1) % 4],
                installation_date=add_days(date(2023, 1, 1), i),
                status="Active",
            )
        )

        operators.append(
            Operator(
                operator_id=make_id(config.run_tag, "OP", i),
                name=f"Operator {i}",
                role=["Shift Lead", "QC", "Machine Tech",
                      "Line Worker"][(i - 1) % 4],
                phone=f"09{rnd.randint(10000000, 99999999)}",
            )
        )

        quality_test_items.append(
            QualityTestItem(
                test_item_id=make_id(config.run_tag, "QTI", i),
                name=f"Quality Metric {i}",
                unit=["%", "pH", "CFU/g", "ppm"][(i - 1) % 4],
                standard_value=Decimal("10") + Decimal((i - 1) % 6),
            )
        )

        packaging_lines.append(
            PackagingLine(
                line_id=make_id(config.run_tag, "LINE", i),
                line_name=f"Packaging Line {config.run_tag}-{i}",
                capacity_per_hour=Decimal("500") + Decimal((i - 1) * 10),
            )
        )

        vehicles.append(
            TransportVehicle(
                vehicle_id=make_id(config.run_tag, "VEH", i),
                license_plate=f"85C-{rnd.randint(10000, 99999)}.{rnd.randint(10, 99)}",
                capacity=Decimal("3000") + Decimal((i - 1) * 20),
            )
        )

    entities = MasterDataEntities(
        farms=farms,
        warehouses=warehouses,
        factories=factories,
        step_types=step_types,
        machines=machines,
        operators=operators,
        quality_test_items=quality_test_items,
        packaging_lines=packaging_lines,
        vehicles=vehicles,
    )

    refs = MasterDataRefs(
        farm_ids=[x.farm_id for x in farms],
        warehouse_ids=[x.warehouse_id for x in warehouses],
        factory_ids=[x.factory_id for x in factories],
        step_type_ids=[x.step_type_id for x in step_types],
        machine_ids=[x.machine_id for x in machines],
        operator_ids=[x.operator_id for x in operators],
        quality_test_item_ids=[x.test_item_id for x in quality_test_items],
        packaging_line_ids=[x.line_id for x in packaging_lines],
        vehicle_ids=[x.vehicle_id for x in vehicles],
    )

    return entities, refs
