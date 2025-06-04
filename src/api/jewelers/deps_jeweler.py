from fastapi import Path, Depends, HTTPException, status

# from src.database import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from src.models.db_helper import db_helper
from src.models.models import *

from . import crud_jew


async def jeweler_by_id(
    jeweler_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> JewelersOrm:
    jeweler = await crud_jew.get_jeweler(session=session, jeweler_id=jeweler_id)
    if jeweler is not None:
        return jeweler

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Jeweler {jeweler_id} not found!",
    )
