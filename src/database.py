from fastapi import Depends
from typing import Annotated
from .config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


# async def get_session():
#     async with async_session_factory() as session:
#         yield session


# SessionDep = Annotated[AsyncSession, Depends(get_session)]


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}
