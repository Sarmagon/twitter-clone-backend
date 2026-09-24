"""
Роутер для управления лайками.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.likes import create_like, delete_like
from app.crud.tweets import get_tweet_by_id
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.like import LikeResponse

router = APIRouter()


@router.post("/api/tweets/{tweet_id}/likes", response_model=LikeResponse)
async def like_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Поставить лайк на твит."""
    if await get_tweet_by_id(db, tweet_id) is None:
        raise HTTPException(404, "Tweet not found")
    await create_like(db, user_id=current_user.id, tweet_id=tweet_id)
    return {"result": True}


@router.delete("/api/tweets/{tweet_id}/likes", response_model=LikeResponse)
async def unlike_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Убрать лайк с твита."""
    await delete_like(db, user_id=current_user.id, tweet_id=tweet_id)
    return {"result": True}
