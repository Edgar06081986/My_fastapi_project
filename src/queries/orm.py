import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import   select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from  src.models import JewelersOrm, ClientsOrm, OrdersOrm, Workload
from src.database import Base, async_engine, async_session_factory
from src.schemas import ( JewelersAddDTO,JewelersDTO,JewelersRelDTO,ClientsAddDTO,ClientsDTO,ClientsRelDTO,OrdersAddDTO,OrdersDTO,OrdersRelDTO)
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
    async def insert_clients(username:str,email:EmailStr,client_avatar:Optional[bytes],phone_number:str):
        async with async_session_factory() as session:
            add_client= ClientsOrm(username=username,email=email,client_avatar=client_avatar,phone_number=phone_number)
            session.add_all([add_client])
            # flush взаимодействует с БД, поэтому пишем await
            # await session.flush()
            await session.commit()
            
    
    @staticmethod
    async def insert_jewelers(username:str,workload:Workload,phone_number:str,adress:str,jeweler_avatar:Optional[bytes],email: str):
        async with async_session_factory() as session:
            add_jeweler = JewelersOrm(username=username,workload=workload,phone_number=phone_number,adress=adress,jeweler_avatar =jeweler_avatar,email=email)
            session.add_all([add_jeweler])
            # flush взаимодействует с БД, поэтому пишем await
            # await session.flush()
            await session.commit()


            
    @staticmethod
    async def insert_orders(title:str,compensation:Optional[int],workload:Workload,client_id:int,jeweler_id:int):
        async with async_session_factory() as session:
            order_add = OrdersOrm(title=title, compensation=compensation, workload=workload, client_id=client_id,jeweler_id=jeweler_id)
            session.add_all([order_add])
            await session.commit()



    @staticmethod
    async def select_jewelers():
        async with async_session_factory() as session:
            query = select(JewelersOrm)
            result = await session.execute(query)
            jewelers = result.scalars().all()
            print(f"{jewelers=}")

    @staticmethod
    async def update_jeweler(jeweler_id: int, new_username: str = "Misha"):
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

  