import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from queries.orm import AsyncORM

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




async def main():
    if "--orm" in sys.argv and "--async" in sys.argv:
        await AsyncORM.create_tables()
        await AsyncORM.insert_jewelers()
        await AsyncORM.select_jewelers()
        await AsyncORM.update_jeweler()
        await AsyncORM.insert_orders()
        await AsyncORM.insert_clients()
        await AsyncORM.select_clients()
        await AsyncORM.update_client()



def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )
        
    @app.get("/jewelers", tags=["Кандидат"])
    async def get_jewelers():
        workers = AsyncORM.convert_workers_to_dto()
        return workers
        
    @app.get("/orders", tags=["Заказы"])
    async def get_resumes():
        resumes = await AsyncORM.select_resumes_with_all_relationships()
        return resumes
    
    return app
    

app = create_fastapi_app()


if __name__ == "__main__":
    asyncio.run(main())
    if "--webserver" in sys.argv:
        uvicorn.run(
            app="src.main:app",
            reload=True,
        )


        # await AsyncORM.select_resumes_avg_compensation()
        # await AsyncORM.insert_additional_resumes()
        # await AsyncORM.join_cte_subquery_window_func()
        # await AsyncORM.select_workers_with_lazy_relationship()
        # await AsyncORM.select_workers_with_joined_relationship()
        # await AsyncORM.select_workers_with_selectin_relationship()
        # await AsyncORM.select_workers_with_condition_relationship()
        # await AsyncORM.select_workers_with_condition_relationship_contains_eager()
        # await AsyncORM.select_workers_with_relationship_contains_eager_with_limit()
        # await AsyncORM.convert_workers_to_dto()
        # await AsyncORM.add_vacancies_and_replies()
        # await AsyncORM.select_resumes_with_all_relationships()



# from contextlib import asynccontextmanager
# from database import create_tables, delete_tables
# from router import router as tasks_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print("База очищена")
#     await create_tables()
#     print("База готова к работе")
#     yield
#     print("Выключение")


# app = FastAPI(lifespan=lifespan)
# app.include_router(tasks_router)

