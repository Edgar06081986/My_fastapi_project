from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import JewelersOrm
from src.api_v1.jewelers.jew_schemas import UpdateJewelersDTO


async def get_jeweler(session: AsyncSession, jeweler_id: int) -> Optional[JewelersOrm]:
    """Fetch a jeweler by ID."""
    try:
        return await session.get(JewelersOrm, jeweler_id)
    except Exception as e:
        print(f"Error fetching jeweler: {e}")
        return None


async def update_jeweler(
    session: AsyncSession,
    jeweler: JewelersOrm,
    jeweler_update: UpdateJewelersDTO,
    partial: bool = False,
) -> JewelersOrm:
    """Update a jeweler's details."""
    try:
        update_data = jeweler_update.model_dump(exclude_unset=partial)
        for name, value in update_data.items():
            setattr(jeweler, name, value)
        await session.commit()
        return jeweler
    except Exception as e:
        await session.rollback()
        print(f"Error updating jeweler: {e}")
        raise


async def select_jewelers(session: AsyncSession) -> list[JewelersOrm]:
    """Fetch all jewelers."""
    query = select(JewelersOrm)
    result = await session.execute(query)
    return result.scalars().all()


async def delete_jeweler(session: AsyncSession, jeweler: JewelersOrm) -> None:
    """Delete a jeweler."""
    try:
        await session.delete(jeweler)
        await session.commit()
    except Exception as e:
        await session.rollback()
        print(f"Error deleting jeweler: {e}")
        raise


#
# async def insert_jewelers(
#     username: str,
#     workload: Workload,
#     phone_number: str,
#     address: str,
#     jeweler_avatar: Optional[bytes],
#     email: str,
# ):
#     async with async_session_factory() as session:
#         add_jeweler = JewelersOrm(
#             username=username,
#             workload=workload,
#             phone_number=phone_number,
#             address=address,
#             jeweler_avatar=jeweler_avatar,
#             email=email,
#         )
#         session.add_all([add_jeweler])
#         # flush взаимодействует с БД, поэтому пишем await
#         # await session.flush()
#         await session.commit()


# async def select_jewelers():
#     async with async_session_factory() as session:
#         query = select(JewelersOrm)
#         result = await session.execute(query)
#         jewelers = result.scalars().all()
#         print(f"{jewelers=}")


#
# async def update_jeweler(jeweler_id: int, new_username: str = "Misha"):
#     async with async_session_factory() as session:
#         jeweler_michael = await session.get(models.JewelersOrm, jeweler_id)
#         jeweler_michael.username = new_username
#         await session.refresh(jeweler_michael)
#         await session.commit()
#
# #
# async def convert_jewelers_to_dto():
#     async with async_session_factory() as session:
#         query = select(JewelersOrm)  # without relathionship
#         res = session.execute(query)
#         result_orm = res.scalars().all()
#         result_dto = [
#             JewelersDTO.model_validate(row, from_attributes=True) for row in result_orm
#         ]
#         print(f"{result_dto=}")
#         return result_dto


# async def convert_jewelers_to_dto_0():
#     async with async_session_factory() as session:
#         query = (
#             select(JewelersOrm)
#             .options(selectinload(JewelersOrm.orders))  # with relathionship
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
