"""Async database engine and request sessions."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url("postgresql+asyncpg"), pool_pre_ping=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base for all database tables."""


async def get_session() -> AsyncIterator[AsyncSession]:
    """Close and roll back uncommitted work after every request."""
    async with async_session() as session:
        yield session
