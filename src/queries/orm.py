from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from models import JewelersOrm, ClientsOrm, OrdersOrm, Workload
from database import Base, async_engine, async_session_factory


class AsyncORM:
    # Асинхронный вариант, не показанный в видео
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            
    
    @staticmethod
    async def insert_jewelers():
        async with async_session_factory() as session:
            worker_jack = JewelersOrm(username="Jack")
            worker_michael = JewelersOrm(username="Michael")
            session.add_all([worker_jack, worker_michael])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_jewelers():
        async with async_session_factory() as session:
            query = select(JewelersOrm)
            result = await session.execute(query)
            jewelers = result.scalars().all()
            print(f"{jewelers=}")

    @staticmethod
    async def update_jeweler(jeweler_id: int = 2, new_username: str = "Misha"):
        async with async_session_factory() as session:
            jeweler_michael = await session.get(JewelersOrm, jeweler_id)
            jeweler_michael.username = new_username
            await session.refresh(jeweler_michael)
            await session.commit()

    @staticmethod
    async def convert_jewelers_to_dto():
        async with async_session_factory() as session:
            query = (
                select(JewelersOrm)
                .options(selectinload(JewelersOrm.resumes))
                .limit(2)
            )        


    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    @staticmethod
    async def insert_clients():
        async with async_session_factory() as session:
            client_jack = ClientsOrm(username="Jack")
            client_michael = ClientsOrm(username="Michael")
            session.add_all([client_jack, client_michael])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_clients():
        async with async_session_factory() as session:
            query = select(ClientsOrm)
            result = await session.execute(query)
            clients = result.scalars().all()
            print(f"{clients=}")

    @staticmethod
    async def update_client(client_id: int = 2, new_username: str = "Misha"):
        async with async_session_factory() as session:
            client_michael = await session.get(ClientsOrm, client_id)
            client_michael.username = new_username
            await session.refresh(client_michael)
            await session.commit()


    @staticmethod
    async def convert_clients_to_dto():
        async with async_session_factory() as session:
            query = (
                select(ClientsOrm)
                .options(selectinload(JewelersOrm.resumes))
                .limit(2)
            )        

    @staticmethod
    async def insert_orders():
        async with async_session_factory() as session:
            order_jack_1 = OrdersOrm(
                title="Изготовить кольцо", compensation=50000, workload=Workload.fulltime, client_id=1)
            order_jack_2 = OrdersOrm(
                title="Сделать пару обручалок", compensation=150000, workload=Workload.fulltime, client_id=1)
            order_michael_1 = OrdersOrm(
                title="Нужен браслет", compensation=250000, workload=Workload.parttime, client_id=2)
            order_michael_2 = OrdersOrm(
                title="Цепь бисмарк", compensation=300000, workload=Workload.fulltime, client_id=2)
            session.add_all([order_jack_1, order_jack_2, 
                             order_michael_1, order_michael_2])
            await session.commit()

  