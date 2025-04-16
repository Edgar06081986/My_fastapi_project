import os
import boto3
from fastapi import FastAPI,HTTPException,UploadFile,File
import asyncio
import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.queries.orm import AsyncORM
from src.schemas import JewelersAddDTO,JewelersDTO,ClientsAddDTO,ClientsDTO,OrdersAddDTO,OrdersDTO
import uvicorn
from src.database import SessionDep,async_engine
from src.models import *
from sqlalchemy import select
# from dotenv import load_dotenv
from src.config import yc_settings

app = FastAPI()




@app.post("/setup",summary="Установка базы")
async def setup_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok":True}


# load_dotenv()  # Загружает переменные из .env


# 1. Создаём сессию с настройками доступа к Yandex Cloud
session = boto3.session.Session()

# 2. Создаём клиент для S3, указывая Yandex-эндпоинт
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',  # Особенность Yandex Cloud
    aws_access_key_id=yc_settings.ACCESS_KEY, # Key ID из сервисного аккаунта
    aws_secret_access_key=yc_settings.SECRET_KEY,  # Secret Key
    )



BUCKET_NAME = "app-3djewelers"


@app.post("/jewelers/")
async def add_jeweler(
    username: str,
    email: str,
    workload: Workload,
    session: SessionDep,  # Добавляем зависимость сессии
    phone_number: Optional[str] = None,
    address: Optional[str] = None,
    avatar: Optional[UploadFile] = File(None)
):
    avatar_url = None
    
    if avatar:
        # Проверка типа файла
        if not avatar.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(400, "Only JPG/PNG images allowed")
        
        # Загрузка в S3
        file_key = f"avatars/{username}_{avatar.filename}"
        s3.upload_fileobj(avatar.file, "app-3djewelers", file_key)
        avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"

    # Создание DTO
        data = JewelersAddDTO(
        username=username,
        email=email,
        phone_number=phone_number,
        address=address,
        workload=workload,
        jeweler_avatar_url=str(avatar_url) 
    )
    
    # Преобразование в SQLAlchemy модель
    new_jeweler = JewelersOrm(**data.model_dump())
    
    # Сохранение в БД (теперь с асинхронными вызовами)
    session.add(new_jeweler)
    await session.commit()
    await session.refresh(new_jeweler)
    
    return {"message": "Jeweler created successfully",'new_jeweler':new_jeweler}

# @app.post("/jewelers", tags=["Ювелиры"],summary= " Добавить ювелира")
# async def add_jeweler(data: JewelersAddDTO,session:SessionDep):
#     # add_jew = await  AsyncORM.insert_jewelers(username=data.username,workload=data.workload,adress=data.adress,email=data.email,phone_number=data.phone_number,jeweler_avatar=data.jeweler_avatar)
#     # return {"ok":True}
#     new_jeweler = JewelersOrm(username=data.username,workload=data.workload,adress=data.adress,email=data.email,phone_number=data.phone_number)   
#     session.add(new_jeweler)
#     await session.commit()
#     return {"ok":True}

@app.get("/jewelers", tags=["Ювелиры"],summary="Получить всех ювелиров")
async def get_jewelers(session:SessionDep):
    query = select(JewelersOrm)
    result = await session.execute(query)
    return result.scalars().all()

# async def read_jewelers(jewelers:JewelersAddDTO):
#     result = await AsyncORM.convert_jewelers_to_dto()
#     return result

# @app.get("/jewelers/{jeweler_id}", tags=["Ювелир"],summary="Получить конкретного ювелира")
# async def get_jeweler(jeweler_id: JewelersDTO):  # ← Указываем тип (int, str, UUID и т.д.)
    
#     return {"jeweler_id": jeweler_id}



 # 1. Создаём сессию с настройками доступа к Yandex Cloud
# session = boto3.session.Session()

 # 2. Создаём клиент для S3, указывая Yandex-эндпоинт
# s3 = session.client(
#     service_name='s3',
#     endpoint_url='https://storage.yandexcloud.net',  # Особенность Yandex Cloud
#     aws_access_key_id='YOUR_ACCESS_KEY',  # Key ID из сервисного аккаунта
#     aws_secret_access_key='YOUR_SECRET_KEY',  # Secret Key

    

# @app.post("/clients", tags=["Клиенты"],summary="Добавить клиента")
# async def add_client(data: ClientsAddDTO,session:SessionDep,avatar: Optional[UploadFile] = File(None),
# ):
#     avatar_url = None
    
#     if avatar:
#         # Проверка типа файла
#         if not avatar.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#             raise HTTPException(400, "Only JPG/PNG images allowed")
        
#         # Загрузка в S3
#         file_key = f"avatars/{data.username}_{avatar.filename}"
#         s3.upload_fileobj(data.avatar.file, "app-3djewelers", file_key)
#         avatar_url = f"https://storage.yandexcloud.net/your-bucket/{file_key}"
#         data.client_avatar_url=avatar_url
    
#     new_client=ClientsOrm(username=data.username,email=data.email,phone_number=data.phone_number)
#     session.add(new_client)
#     await session.commit()
#     return {"Клиент создан":True}


@app.get("/clients", tags=["Клиенты"],summary="Получить всех клиентов")
async def get_clients(session:SessionDep):
    query = select(ClientsOrm)
    result = await session.execute(query)
    return result.scalars().all()

# # @app.get("/clients", tags=["Клиенты"],summary="Получить всех клиентов")
# # async def read_clients():
# #     clients = await AsyncORM.convert_clients_to_dto()
# #     return clients
    


# # @app.get("/clients/{client_id}", tags=["Клиенты"],summary="Получить конкретного клиента")
# # async def get_client():
# #     pass


# @app.post("/orders", tags=["Заказы"],summary="Добавить заказ")
# async def add_client(new_order: OrdersAddDTO):
#     add_order = await AsyncORM.insert_orders(title =new_order.title,compensation=new_order.compensation,workload=new_order.workload,client_id=new_order.client_id,jeweler_id=new_order.jeweler_id)
#     return add_order                                          


# @app.post("/orders", tags=["Заказы"],summary="Добавить заказ")
# async def add_order(data: OrdersAddDTO,session:SessionDep):
#     new_order=ClientsOrm(title =data.title,compensation=data.compensation,workload=data.workload,client_id=data.client_id,jeweler_id=data.jeweler_id)
#     session.add(new_order)
#     await session.commit()
#     return {"Заказ создан":True}


@app.get("/orders", tags=["Заказы"],summary="Получить все заказы")
async def get_orders(session:SessionDep):
    query = select(OrdersOrm)
    result = await session.execute(query)
    return result.scalars().all()



# # @app.get("/orders", tags=["Заказы"],summary="Получить все заказы")
# # async def read_orders():
# #     res = await AsyncORM.select_orders()
# #     return res


# # # @app.get("/orders/{order_id}", tags=["Заказы"],summary="Получить конкретный заказ")
# # # async def get_order():
# # #     pass



if __name__ == "__main__":    
    uvicorn.run("src.main:app",reload=True)
    
# # if __name__ == "__main__":
# #     asyncio.run(main())  
# #     if "--webserver" in sys.argv:
# #         uvicorn.run(
# #             "src.main:app",
# #             reload=True,)
