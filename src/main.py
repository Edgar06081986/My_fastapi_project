import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '.'))
from orm import AsyncORM
from schemas import JewelersAddDTO,JewelersDTO,ClientsAddDTO,ClientsDTO,OrdersAddDTO,OrdersDTO
import uvicorn
from fastapi import FastAPI,HTTPException
from models import JewelersOrm,ClientsOrm,OrdersOrm


async def main():
    AsyncORM.create_tables()


app = FastAPI()



@app.post("/jewelers", tags=["Ювелиры"],summary= " Добавить ювелира")
async def add_jeweler(new_jeweler: JewelersAddDTO):
    add_jew = await  AsyncORM.insert_jewelers(username=new_jeweler.username,workload=new_jeweler.workload,adress=new_jeweler.adress,email=new_jeweler.email,phone_number=new_jeweler.phone_number,jeweler_avatar=new_jeweler.jeweler_avatar)
    return add_jew



@app.get("/jewelers", tags=["Ювелиры"],summary="Получить всех ювелиров")
async def read_jewelers(jewelers:JewelersAddDTO):
    result = await AsyncORM.convert_jewelers_to_dto()
    return result
    


# @app.get("/jewelers/{jeweler_id}", tags=["Ювелир"],summary="Получить конкретного ювелира")
# async def get_jeweler(jeweler_id: JewelersDTO):
#     for jeweler in JewelersDTO:
#         if jeweler["id"]== jeweler_id:
#             return jeweler
#         raise HTTPException(status_code=404,detail=" Ювелира с таким идентификатором несуществует")

    

@app.post("/clients", tags=["Клиенты"],summary="Добавить клиента")
async def add_client(new_client: ClientsAddDTO):
    add_client = await AsyncORM.insert_clients(username=new_client.username,email=new_client.email,phone_number=new_client.phone_number,client_avatar=new_client.client_avatar)

    return add_client,{"Клиент создан":True}



# @app.get("/clients", tags=["Клиенты"],summary="Получить всех клиентов")
# async def read_clients():
#     clients = await AsyncORM.convert_clients_to_dto()
#     return clients
    


# @app.get("/clients/{client_id}", tags=["Клиенты"],summary="Получить конкретного клиента")
# async def get_client():
#     pass


@app.post("/orders", tags=["Заказы"],summary="Добавить заказ")
async def add_client(new_order: OrdersAddDTO):
    add_order = await AsyncORM.insert_orders(title =new_order.title,compensation=new_order.compensation,workload=new_order.workload,client_id=new_order.client_id,jeweler_id=new_order.jeweler_id)
    return add_order                                          



# @app.get("/orders", tags=["Заказы"],summary="Получить все заказы")
# async def read_orders():
#     res = await AsyncORM.select_orders()
#     return res


# @app.get("/orders/{order_id}", tags=["Заказы"],summary="Получить конкретный заказ")
# async def get_order():
#     pass



if __name__== "__main__":
    uvicorn.run(app)
