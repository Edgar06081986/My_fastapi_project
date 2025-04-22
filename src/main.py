from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api_v1.clients.end_client import router as client_router
from src.models.base import Base
from src.api_v1.orders.end_order import router as order_router
from src.api_v1.jewelers.end_jeweler import router as jeweler_router
import uvicorn
from src.models.db_helper import db_helper

# from src.database import SessionDep, async_engine
from src.config import yc_settings, settings
from src.api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(router=router_v1, prefix=yc_settings.api_v1_prefix_2)




if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)

# # if __name__ == "__main__":
# #     asyncio.run(main())
# #     if "--webserver" in sys.argv:
# #         uvicorn.run(
# #             "src.main:app",
# #             reload=True,)
