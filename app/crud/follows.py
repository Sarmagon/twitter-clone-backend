"""Idempotent follow operations backed by a unique constraint."""

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.follow import Follow


async def get_follow(db: AsyncSession, follower_id: int, following_id: int):
    """Find an existing relationship."""
    return await db.scalar(
        select(Follow).where(Follow.follower_id == follower_id, Follow.following_id == following_id)
    )


async def create_follow(db: AsyncSession, follower_id: int, following_id: int):
    """Insert once, including when requests race."""
    existing = await get_follow(db, follower_id, following_id)
    if existing is not None:
        return existing
    item = Follow(follower_id=follower_id, following_id=following_id)
    db.add(item)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        existing = await get_follow(db, follower_id, following_id)
        if existing is None:
            raise
        return existing
    await db.refresh(item)
    return item


async def delete_follow(db: AsyncSession, follower_id: int, following_id: int) -> None:
    """Removing an absent relationship is also successful."""
    await db.execute(
        delete(Follow).where(Follow.follower_id == follower_id, Follow.following_id == following_id)
    )
    await db.commit()
