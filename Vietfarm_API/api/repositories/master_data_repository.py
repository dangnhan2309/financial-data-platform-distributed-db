from api.models.master_data_models import (
    AloeFarm,
    Factory,
    Machine,
    QualityTestItem,
    StepType,
    Warehouse,
)
from api.repositories.base_repository import BaseRepository


aloe_farm_repository = BaseRepository[AloeFarm](AloeFarm)
factory_repository = BaseRepository[Factory](Factory)
warehouse_repository = BaseRepository[Warehouse](Warehouse)
step_type_repository = BaseRepository[StepType](StepType)
machine_repository = BaseRepository[Machine](Machine)
quality_test_item_repository = BaseRepository[QualityTestItem](QualityTestItem)
