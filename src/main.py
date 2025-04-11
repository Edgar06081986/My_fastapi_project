import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from orm import AsyncORM
from schemas import JewelersAddDTO,JewelersDTO,ClientsAddDTO,ClientsDTO,OrdersAddDTO,OrdersDTO
import uvicorn
from fastapi import FastAPI



app = FastAPI()



@app.get("/jewelers", tags=["Ювелир"])
async def read_jewelers():
    jewelers = await AsyncORM.convert_jewelers_to_dto()
    return jewelers
    
    


@app.post("/jewelers", tags=["Ювелир"])
async def add_jeweler(new_jeweler: JewelersAddDTO)-> JewelersDTO:
    add_jew = await  AsyncORM.insert_jewelers(username=new_jeweler.username,workload=new_jeweler.workload,adress=new_jeweler.adress,email=new_jeweler.email,phone_number=new_jeweler.phone_number,jeweler_avatar=new_jeweler.jeweler_avatar)
    return add_jeweler




@app.get("/jewelers", tags=["Ювелир"])
async def read_jewelers():
    jewelers = await AsyncORM.convert_jewelers_to_dto()
    return jewelers



@app.get("/jewelers/{jeweler_id}", tags=["Ювелир"])
async def get_jeweler():
    pass
    


@app.post("/clients", tags=["Клиент"])
async def add_client(new_client: ClientsAddDTO):
    add_client = await AsyncORM.insert_clients()
    return add_client



@app.get("/clients", tags=["Клиент"])
async def read_clients():
    clients = await AsyncORM.convert_clients_to_dto()
    return clients
    


@app.get("/clients/{client_id}", tags=["Клиент"])
async def get_client():
    pass

    

@app.get("/orders", tags=["Заказы"])
async def read_orders():
    res = await AsyncORM.select_resumes_with_all_relationships()
    return res


@app.get("/orders/{order_id}", tags=["Заказы"])
async def get_order():
    pass



if __name__== "__main__":
    uvicorn.run("main:app",reload=False)
