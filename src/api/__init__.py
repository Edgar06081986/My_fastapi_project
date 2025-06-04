from fastapi import APIRouter

from src.api.end_jeweler import router as jeweler_router
from src.api.end_client import router as client_router
from .orders.end_order import router as order_router
from .orders import *
from .clients import *
from .jewelers import *

router = APIRouter()
router.include_router(router=jeweler_router)
router.include_router(router=client_router)
router.include_router(router=order_router)
