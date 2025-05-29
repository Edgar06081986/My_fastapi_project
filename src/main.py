from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api_v1.clients.end_client import router as client_router
from src.api_v1.orders.end_order import router as order_router
from src.api_v1.jewelers.end_jeweler import router as jeweler_router
from src.demo_auth.demo_jwt_auth import router as demo_jwt_auth_router
from src.config import yc_settings, settings
from src.logger import logger
import asyncio
from src.bot.main import start_bot


logger.info("FastAPI приложение запущено")
logger.warning("Что-то пошло не так")
logger.error("Произошла ошибка")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Запуск aiogram бота в фоне")
    asyncio.create_task(start_bot())
    yield
    logger.info("🛑 Остановка приложения")


app = FastAPI(lifespan=lifespan)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно разрешить все origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(demo_jwt_auth_router)
app.include_router(client_router, prefix=settings.api_v1_prefix)
app.include_router(order_router, prefix=settings.api_v1_prefix)
app.include_router(jeweler_router, prefix=settings.api_v1_prefix)

# Дополнительный префикс только если нужен
if settings.api_v1_prefix != yc_settings.api_v1_prefix_2:
    app.include_router(client_router, prefix=yc_settings.api_v1_prefix_2)
    app.include_router(order_router, prefix=yc_settings.api_v1_prefix_2)
    app.include_router(jeweler_router, prefix=yc_settings.api_v1_prefix_2)
