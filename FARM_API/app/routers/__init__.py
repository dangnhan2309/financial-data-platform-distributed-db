from fastapi import APIRouter
from .farm import router as farm_router
from .iot import router as iot_router
from .cultivation import router as cultivation_router
from .catalog import router as catalog_router
from .harvest import router as harvest_router
from .procurement import router as procurement_router
from .quality import router as quality_router

router = APIRouter()

router.include_router(farm_router, tags=["Farm Management"])
router.include_router(iot_router, tags=["IoT System"])
router.include_router(cultivation_router, tags=["Cultivation"])
router.include_router(catalog_router, tags=["Catalog"])
router.include_router(harvest_router, tags=["Harvest"])
router.include_router(procurement_router, tags=["Procurement"])
router.include_router(quality_router, tags=["Quality Control"])
