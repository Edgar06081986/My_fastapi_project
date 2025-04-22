from typing import Optional
from src.database import SessionDep
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database import async_session_factory
from src.models.models import JewelersOrm, Workload
import src.models as models
from src.api_v1.jewelers.jew_schemas import JewelersRelDTO, JewelersDTO


async def insert_jewelers(
    username: str,
    workload: Workload,
    phone_number: str,
    adress: str,
    jeweler_avatar: Optional[bytes],
    email: str,
):
    async with async_session_factory() as session:
        add_jeweler = JewelersOrm(
            username=username,
            workload=workload,
            phone_number=phone_number,
            adress=adress,
            jeweler_avatar=jeweler_avatar,
            email=email,
        )
        session.add_all([add_jeweler])
        # flush взаимодействует с БД, поэтому пишем await
        # await session.flush()
        await session.commit()


async def select_jewelers():
    async with async_session_factory() as session:
        query = select(JewelersOrm)
        result = await session.execute(query)
        jewelers = result.scalars().all()
        print(f"{jewelers=}")


async def update_jeweler(jeweler_id: int, new_username: str = "Misha"):
    async with async_session_factory() as session:
        jeweler_michael = await session.get(models.JewelersOrm, jeweler_id)
        jeweler_michael.username = new_username
        await session.refresh(jeweler_michael)
        await session.commit()


async def convert_jewelers_to_dto():
    async with async_session_factory() as session:
        query = select(JewelersOrm)  # without relathionship
        res = session.execute(query)
        result_orm = res.scalars().all()
        result_dto = [
            JewelersDTO.model_validate(row, from_attributes=True) for row in result_orm
        ]
        print(f"{result_dto=}")
        return result_dto


async def convert_jewelers_to_dto_0():
    async with async_session_factory() as session:
        query = (
            select(JewelersOrm)
            .options(selectinload(JewelersOrm.orders))  # with relaithionship
            .limit(2)
        )
        res = session.execute(query)
        result_orm = res.scalars().all()
        print(f"{result_orm=}")
        result_dto = [
            JewelersRelDTO.model_validate(row, from_attributes=True)
            for row in result_orm
        ]
        print(f"{result_dto=}")
        return result_dto


async def delete_jeweler(
    session: SessionDep,
    jeweler: JewelersOrm,
) -> None:
    await session.delete(jeweler)
    await session.commit()