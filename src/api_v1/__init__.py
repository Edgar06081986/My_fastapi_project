from fastapi import APIRouter

from .jewelers.end_jeweler import router as jeweler_router
from .clients.end_client import router as client_router
from .orders.end_order import router as order_router


router = APIRouter()
router.include_router(router=jeweler_router,)
router.include_router(router=client_router)
router.include_router(router=order_router)
