from typing import Optional
from src.database import async_session_factory,SessionDep
from src.models.models import OrdersOrm, Workload


async def insert_orders(
    title: str,
    compensation: Optional[int],
    workload: Workload,
    client_id: int,
    jeweler_id: int,
):
    async with async_session_factory() as session:
        order_add = OrdersOrm(
            title=title,
            compensation=compensation,
            workload=workload,
            client_id=client_id,
            jeweler_id=jeweler_id,
        )
        session.add_all([order_add])
        await session.commit()


async def select_orders():
    pass






async def delete_order(
    session: SessionDep,
    order: OrdersOrm,
) -> None:
    await session.delete(order)
    await session.commit()

