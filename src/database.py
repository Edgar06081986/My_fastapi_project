from typing import Optional,Annotated
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, and_, func, insert, select, text, update,String

engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
    echo=True,)
new_session = async_sessionmaker(engine, expire_on_commit=False)






async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)


async_session_factory = async_sessionmaker(async_engine)


str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

