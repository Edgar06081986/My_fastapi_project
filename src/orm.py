import os
import sys
from sqlalchemy import   select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from models import JewelersOrm, ClientsOrm, OrdersOrm, Workload
from database import Base, async_engine, async_session_factory
from schemas import ( JewelersAddDTO,JewelersDTO,JewelersRelDTO,ClientsAddDTO,ClientsDTO,ClientsRelDTO,OrdersAddDTO,OrdersDTO,OrdersRelDTO)
from pydantic import BaseModel,EmailStr
from typing import Optional

class AsyncORM:
    # Асинхронный вариант, не показанный в видео
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_clients():
        async with async_session_factory() as session:
            client_tatyana = ClientsOrm(username="Таня Николаева",email="nik-tatyana123@yandex.ru",client_avatar=None,phone_number='+791261662067')
            client_tamara = ClientsOrm(username="Тамара",email="tamara2004@mail.ru",client_avatar=None,phone_number='+79180434556')
            client_buety = ClientsOrm(username="Beautifual Girl",email="beautygirl@gmail.com",client_avatar=None,phone_number='+79999945545')
            client_roman = ClientsOrm(username="RomanMan",email="ramzes@rambler.ru",client_avatar=None,phone_number='+79147678888')
            session.add_all([client_tatyana, client_tamara,client_roman,client_buety])
            # flush взаимодействует с БД, поэтому пишем await
            # await session.flush()
            await session.commit()
            
    
    @staticmethod
    async def insert_jewelers(username:str,workload:Workload,phone_number:str,adress:str,jeweler_avatar:Optional[bytes],email:EmailStr):
        async with async_session_factory() as session:
            add_jeweler = JewelersOrm(username=username,workload=workload,phone_number=phone_number,adress=adress,jeweler_avatar =jeweler_avatar,email=email)
            
            session.add_all([add_jeweler])
            # flush взаимодействует с БД, поэтому пишем await
            # await session.flush()
            await session.commit()


            
    @staticmethod
    async def insert_orders():
        async with async_session_factory() as session:
            order_ring = OrdersOrm(
                title="Отремонитровать  кольцо", compensation=None, workload=Workload.repair, client_id=1,jeweler_id=1)
            order_two_ring = OrdersOrm(
                title="Сделать пару обручалок", compensation=15000, workload=Workload.production, client_id=2,jeweler_id=1)
            order_braclet = OrdersOrm(
                title="Сделать браслет бисмарк и починить кольцо", compensation=25000, workload=Workload.both_add,client_id=3,jeweler_id=2)
            order_errings = OrdersOrm(
                title="серьги молодёжки", compensation=30000, workload=Workload.repair,client_id=4,jeweler_id=2)
            session.add_all([order_ring, order_two_ring, 
                             order_braclet, order_errings])
            await session.commit()



    @staticmethod
    async def select_jewelers():
        async with async_session_factory() as session:
            query = select(JewelersOrm)
            result = await session.execute(query)
            jewelers = result.scalars().all()
            print(f"{jewelers=}")

    @staticmethod
    async def update_jeweler(jeweler_id: int = 3, new_username: str = "Misha"):
        async with async_session_factory() as session:
            jeweler_michael = await session.get(JewelersOrm, jeweler_id)
            jeweler_michael.username = new_username
            await session.refresh(jeweler_michael)
            await session.commit()


    @staticmethod
    async def convert_jewelers_to_dto():
        async with async_session_factory() as session:
            query = (
                select(JewelersOrm)          # without relathionship
            )        
            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [JewelersDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto
        




    @staticmethod
    async def convert_jewelers_to_dto_0():
        async with async_session_factory() as session:
            query = (
                select(JewelersOrm)
                .options(selectinload(JewelersOrm.orders))       #with relaithionship
                .limit(2)
            )        
            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [JewelersRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto
        

    
 
    @staticmethod
    async def select_clients():
        async with async_session_factory() as session:
            query = select(ClientsOrm)
            result = await session.execute(query)
            clients = result.scalars().all()
            print(f"{clients=}")


    @staticmethod
    async def update_client(client_id: int = 2, new_username: str = "Katya"):
        async with async_session_factory() as session:
            client_michael = await session.get(ClientsOrm, client_id)
            client_michael.username = new_username
            await session.refresh(client_michael)
            await session.commit()


    @staticmethod
    async def convert_clients_to_dto_0():
        async with async_session_factory() as session:
            query = (
                select(ClientsOrm)           # без relithionship
            )        
            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [ClientsRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto  


    @staticmethod
    async def convert_clients_to_dto():
        async with async_session_factory() as session:
            query = (
                select(ClientsOrm)
                .options(selectinload(ClientsOrm.orders))   # с relaitionship
                .limit(2)
            )        
            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [JewelersRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto  

  