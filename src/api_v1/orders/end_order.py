from fastapi import APIRouter
from src.database import SessionDep
from src.api_v1.orders import crud_ord
from src.api_v1.orders.ord_schemas import OrdersAddDTO
from sqlalchemy import select
from src.models.models import OrdersOrm

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/orders", summary="Добавить заказ")
async def add_client(new_order: OrdersAddDTO, session: SessionDep):
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


@router.post("/orders", summary="Добавить заказ")
async def add_order(data: OrdersAddDTO, session: SessionDep):
    new_order = OrdersOrm(
        title=data.title,
        compensation=data.compensation,
        workload=data.workload,
        client_id=data.client_id,
        jeweler_id=data.jeweler_id,
    )
    session.add(new_order)
    await session.commit()
    return {"Заказ создан": True}


@router.get("/orders/", summary="Получить все заказы")
async def get_orders(session: SessionDep):
    query = select(OrdersOrm)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/", summary="Получить все заказы")
async def read_orders():
    res = await crud_ord.select_orders()
    return res


@router.get("/orders/{order_id}", tags=["Заказы"], summary="Получить конкретный заказ")
async def get_order():
    pass
