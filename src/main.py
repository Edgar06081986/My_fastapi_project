import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from queries.orm import AsyncORM
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




async def main():
    
    await AsyncORM.create_tables()
    await AsyncORM.insert_jewelers()
    await AsyncORM.insert_clients()
    # await AsyncORM.select_jewelers()
    # await AsyncORM.update_jeweler()
    await AsyncORM.insert_orders()
    # await AsyncORM.select_orders()
    # await AsyncORM.update_order()
    
    # await AsyncORM.select_clients()
    # await AsyncORM.update_client()



# def create_fastapi_app():
#     app = FastAPI(title="FastAPI")
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#     )
        
#     @app.get("/jewelers", tags=["Ювелир"])
#     async def get_jewelers():
#         jewelers = AsyncORM.convert_jewelers_to_dto()
#         return jewelers
    

#     @app.get("/clients", tags=["Клиент"])
#     async def get_jewelers():
#         clients = AsyncORM.convert_clients_to_dto()
#         return clients
        
#     @app.get("/orders", tags=["Заказы"])
#     async def get_resumes():
#         resumes = await AsyncORM.select_resumes_with_all_relationships()
#         return resumes
    
#     return app
    

# app = create_fastapi_app()


if __name__ == "__main__":
    asyncio.run(main())
#     if "--webserver" in sys.argv:
#         uvicorn.run(
#             app="src.main:app",
#             reload=True,
#         )

