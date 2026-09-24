"""Optional demo users for an EMPTY installation only."""

import asyncio

from sqlalchemy import func, select

from app.database import async_session, engine
from app.models import Follow, Tweet, User


async def seed() -> None:
    """Never overwrite or modify an existing user database."""
    async with async_session() as db:
        if await db.scalar(select(func.count()).select_from(User)):
            return
        first = User(
            username="demo", name="Демо-пользователь", api_key="test", hashed_password="!disabled"
        )
        second = User(
            username="colleague",
            name="Коллега",
            api_key="colleague-key",
            hashed_password="!disabled",
        )
        db.add_all([first, second])
        await db.flush()
        db.add(Follow(follower_id=first.id, following_id=second.id))
        db.add(Tweet(author_id=second.id, content="Добро пожаловать! Это демонстрационный твит."))
        await db.commit()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
