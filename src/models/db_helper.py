import asyncio
from typing import Any, AsyncGenerator
from src.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=asyncio.current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(
        self,
    ) -> AsyncGenerator[async_scoped_session[AsyncSession | Any], Any]:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.DATABASE_URL_asyncpg,
    echo=settings.db_echo,
)
print(db_helper.get_scoped_session())
