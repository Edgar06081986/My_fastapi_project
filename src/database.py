from typing import Optional
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, and_, func, insert, select, text, update

engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
    echo=True,)
new_session = async_sessionmaker(engine, expire_on_commit=False)





async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)


async_session_factory = async_sessionmaker(async_engine)