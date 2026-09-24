"""Idempotent like operations backed by a unique constraint."""

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.like import Like


async def get_like(db: AsyncSession, user_id: int, tweet_id: int):
    """Find an existing relationship."""
    return await db.scalar(select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id))


async def create_like(db: AsyncSession, user_id: int, tweet_id: int):
    """Insert once, including when requests race."""
    existing = await get_like(db, user_id, tweet_id)
    if existing is not None:
        return existing
    item = Like(user_id=user_id, tweet_id=tweet_id)
    db.add(item)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        existing = await get_like(db, user_id, tweet_id)
        if existing is None:
            raise
        return existing
    await db.refresh(item)
    return item


async def delete_like(db: AsyncSession, user_id: int, tweet_id: int) -> None:
    """Removing an absent relationship is also successful."""
    await db.execute(delete(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id))
    await db.commit()
