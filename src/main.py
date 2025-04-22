from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api_v1.clients.end_client import router as router_client
from src.models.base import Base
from src.api_v1.orders.end_order import router as router_order
from src.api_v1.jewelers.end_jeweler import router as router_jeweler
import uvicorn
from src.models.db_helper import db_helper

from src.database import SessionDep, async_engine
from src.config import yc_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router_jeweler)
app.include_router(router_order)
app.include_router(router_client)

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)

# # if __name__ == "__main__":
# #     asyncio.run(main())
# #     if "--webserver" in sys.argv:
# #         uvicorn.run(
# #             "src.main:app",
# #             reload=True,)
