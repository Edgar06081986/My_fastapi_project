from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_v1.clients.end_client import router as client_router
from src.models.base import Base
from src.api_v1.orders.end_order import router as order_router
from src.api_v1.jewelers.end_jeweler import router as jeweler_router
import uvicorn
from src.models.db_helper import db_helper

# from src.database import SessionDep, async_engine
from src.config import yc_settings, settings
from src.api_v1 import router as router_v1


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки можно разрешить все origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(client_router, prefix=settings.api_v1_prefix)
app.include_router(order_router, prefix=settings.api_v1_prefix)
app.include_router(jeweler_router, prefix=settings.api_v1_prefix)

# Дополнительный префикс только если нужен
if settings.api_v1_prefix != yc_settings.api_v1_prefix_2:
    app.include_router(client_router, prefix=yc_settings.api_v1_prefix_2)
    app.include_router(order_router, prefix=yc_settings.api_v1_prefix_2)
    app.include_router(jeweler_router, prefix=yc_settings.api_v1_prefix_2)

# # Подключаем роутер с двумя разными префиксами (если они не совпадают)
# if settings.api_v1_prefix != yc_settings.api_v1_prefix_2:
#     app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
#     app.include_router(router=router_v1, prefix=yc_settings.api_v1_prefix_2)
# else:
#     # Если префиксы одинаковые, подключаем только один раз
#     app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)

# # if __name__ == "__main__":
# #     asyncio.run(main())
# #     if "--webserver" in sys.argv:
# #         uvicorn.run(
# #             "src.main:app",
# #             reload=True,)
