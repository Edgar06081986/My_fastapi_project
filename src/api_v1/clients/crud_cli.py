from typing import Optional
from pydantic import EmailStr
from sqlalchemy import select
from src.database import SessionDep
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from src.database import async_session_factory
from src.models.models import ClientsOrm
from src.api_v1.clients.cli_schemas import ClientsRelDTO
from src.api_v1.jewelers.jew_schemas import JewelersRelDTO


async def get_clients(session: SessionDep) -> list[ClientsOrm]:
    stmt = select(ClientsOrm).order_by(ClientsOrm.id)
    result: Result = await session.execute(stmt)
    clients = result.scalars().all()
    return list(clients)


async def get_client(session: SessionDep, client_id: int) -> ClientsOrm| None:
    return await session.get(ClientsOrm, client_id)


# async def insert_clients(
#     username: str,
#     email: EmailStr,
#     client_avatar: Optional[bytes],
#     phone_number: str,
# ):
#     async with async_session_factory() as session:
#         add_client = ClientsOrm(
#             username=username,
#             email=email,
#             client_avatar=client_avatar,
#             phone_number=phone_number,
#         )
#         session.add_all([add_client])
#         # flush взаимодействует с БД, поэтому пишем await
#         # await session.flush()
#         await session.commit()


# async def select_clients():
#     async with async_session_factory() as session:
#         query = select(ClientsOrm)
#         result = await session.execute(query)
#         clients = result.scalars().all()
#         print(f"{clients=}")


# async def update_client(client_id: int = 2, new_username: str = "Katya"):
#     async with async_session_factory() as session:
#         client_michael = await session.get(ClientsOrm, client_id)
#         client_michael.username = new_username
#         await session.refresh(client_michael)
#         await session.commit()


# async def convert_clients_to_dto_0():
#     async with async_session_factory() as session:
#         query = select(ClientsOrm)  # без relithionship
#         res = session.execute(query)
#         result_orm = res.scalars().all()
#         print(f"{result_orm=}")
#         result_dto = [
#             ClientsRelDTO.model_validate(row, from_attributes=True)
#             for row in result_orm
#         ]
#         print(f"{result_dto=}")
#         return result_dto


# async def convert_clients_to_dto():
#     async with async_session_factory() as session:
#         query = (
#             select(ClientsOrm)
#             .options(selectinload(ClientsOrm.orders))  # с relaitionship
#             .limit(2)
#         )
#         res = session.execute(query)
#         result_orm = res.scalars().all()
#         print(f"{result_orm=}")
#         result_dto = [
#             JewelersRelDTO.model_validate(row, from_attributes=True)
#             for row in result_orm
#         ]
#         print(f"{result_dto=}")
#         return result_dto


async def delete_client(
    session: SessionDep,
    client: ClientsOrm,
) -> None:
    await session.delete(client)
    await session.commit()