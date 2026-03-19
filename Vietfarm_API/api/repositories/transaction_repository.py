from api.models.farming_models import RawMaterialInspection
from api.models.processing_models import AloeProcessingBatch, FermentationLog
from api.models.production_models import Inventory
from api.models.quality_models import QualityTestResult
from api.repositories.base_repository import BaseRepository


aloe_processing_batch_repository = BaseRepository[AloeProcessingBatch](
    AloeProcessingBatch)
raw_material_inspection_repository = BaseRepository[RawMaterialInspection](
    RawMaterialInspection)
fermentation_log_repository = BaseRepository[FermentationLog](FermentationLog)
inventory_repository = BaseRepository[Inventory](Inventory)
quality_test_result_repository = BaseRepository[QualityTestResult](
    QualityTestResult)
