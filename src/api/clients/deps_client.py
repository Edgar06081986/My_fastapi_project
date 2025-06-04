from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

# from src.database import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db_helper import db_helper
from src.models.models import *

from . import crud_cli


async def client_by_id(
    client_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ClientsOrm:
    client = await crud_cli.get_client(session=session, client_id=client_id)
    if client is not None:
        return client

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client {client_id} not found!",
    )
