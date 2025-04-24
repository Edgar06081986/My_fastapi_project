from fastapi import APIRouter, Depends, HTTPException

# from src.database import SessionDep
from src.api_v1.orders import crud_ord
from src.api_v1.orders.ord_schemas import OrdersAddDTO
from sqlalchemy import select
from src.models.models import OrdersOrm
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db_helper import db_helper

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", summary="Добавить заказ")
async def add_client(
    new_order: OrdersAddDTO,
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),  # Добавляем зависимость сессии
):
    """Добавить новый заказ в БД."""
    # Проверка типа файла
    if not new_order.title:
        raise HTTPException(400, "Title is required")
    if not new_order.compensation:
        raise HTTPException(400, "Compensation is required")
    if not new_order.workload:
        raise HTTPException(400, "Workload is required")
    if not new_order.client_id:
        raise HTTPException(400, "Client ID is required")
    ad_order = await crud_ord.insert_orders(
        title=new_order.title,
        compensation=new_order.compensation,
        workload=new_order.workload,
        client_id=new_order.client_id,
        jeweler_id=new_order.jeweler_id,
    )
    session.add(ad_order)
    await session.commit()
    return ad_order


# @router.post("/", summary="Добавить заказ")
# async def add_order(data: OrdersAddDTO, session: AsyncSession):
#     new_order = OrdersOrm(
#         title=data.title,
#         compensation=data.compensation,
#         workload=data.workload,
#         client_id=data.client_id,
#         jeweler_id=data.jeweler_id,
#     )
#     session.add(new_order)
#     await session.commit()
#     return {"Заказ создан": True}


@router.get("/", summary="Получить все заказы")
async def get_orders(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Получить все заказы из БД."""
    # Выполняем запрос к базе данных
    query = select(OrdersOrm)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/", summary="Получить все заказы")
async def read_orders():
    res = await crud_ord.select_orders()
    return res
