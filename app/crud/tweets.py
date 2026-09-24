"""Feed queries and atomic tweet creation."""

from fastapi import HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.follow import Follow
from app.models.like import Like
from app.models.media import Media
from app.models.tweet import Tweet


async def get_tweets(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100, author_id: int | None = None
):
    """Feed: followed authors ranked by likes; profile: one author's tweets."""
    popularity = (
        select(func.count(Like.id))
        .where(Like.tweet_id == Tweet.id)
        .correlate(Tweet)
        .scalar_subquery()
    )
    query = select(Tweet).options(
        selectinload(Tweet.author),
        selectinload(Tweet.medias),
        selectinload(Tweet.likes).selectinload(Like.user),
    )
    if author_id is None:
        query = query.where(
            Tweet.author_id.in_(select(Follow.following_id).where(Follow.follower_id == user_id))
        )
        query = query.order_by(popularity.desc(), Tweet.created_at.desc(), Tweet.id.desc())
    else:
        query = query.where(Tweet.author_id == author_id).order_by(
            Tweet.created_at.desc(), Tweet.id.desc()
        )
    return (await db.scalars(query.offset(skip).limit(limit))).all()


async def get_tweet_by_id(db: AsyncSession, tweet_id: int):
    """Get a tweet for permission checks."""
    return await db.scalar(select(Tweet).where(Tweet.id == tweet_id))


async def create_tweet(
    db: AsyncSession, author_id: int, content: str, media_ids: list[int] | None = None
):
    """Validate and attach all images in the same transaction as the tweet."""
    ids = media_ids or []
    medias = []
    if ids:
        medias = (
            await db.scalars(
                select(Media).where(Media.id.in_(ids)).order_by(Media.id).with_for_update()
            )
        ).all()
        if len(medias) != len(ids):
            raise HTTPException(404, "Media not found")
        if any(m.owner_id != author_id for m in medias):
            raise HTTPException(403, "Media belongs to another user")
        if any(m.tweet_id is not None for m in medias):
            raise HTTPException(409, "Media is already attached")
    item = Tweet(author_id=author_id, content=content)
    db.add(item)
    await db.flush()
    for media in medias:
        media.tweet_id = item.id
    await db.commit()
    await db.refresh(item)
    return item


async def delete_tweet(db: AsyncSession, tweet_id: int) -> None:
    """Delete the tweet; database cascades likes and detaches media."""
    await db.execute(delete(Tweet).where(Tweet.id == tweet_id))
    await db.commit()


def tweet_response(tweet: Tweet) -> dict:
    """Serialize only already-loaded relationships."""
    return {
        "id": tweet.id,
        "content": tweet.content,
        "attachments": ["/" + m.file_path.lstrip("/") for m in tweet.medias],
        "author": {"id": tweet.author.id, "name": tweet.author.name or ""},
        "likes": [{"user_id": item.user_id, "name": item.user.name or ""} for item in tweet.likes],
        "created_at": tweet.created_at,
    }
