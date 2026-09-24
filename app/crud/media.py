"""Media metadata operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import Media


async def get_media_by_id(db: AsyncSession, media_id: int):
    """Find uploaded media."""
    return await db.scalar(select(Media).where(Media.id == media_id))


async def create_media(
    db: AsyncSession, file_path: str, owner_id: int, tweet_id: int | None = None
):
    """Persist upload ownership."""
    item = Media(file_path=file_path, owner_id=owner_id, tweet_id=tweet_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
