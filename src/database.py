from typing import Optional
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
    echo=True,)
new_session = async_sessionmaker(engine, expire_on_commit=False)





async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)