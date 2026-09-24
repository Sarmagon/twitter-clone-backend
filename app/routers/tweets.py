"""Tweet endpoints matching the supplied contract."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tweets import create_tweet, delete_tweet, get_tweet_by_id, get_tweets, tweet_response
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.tweet import TweetCreate, TweetCreatedResponse, TweetListResponse

router = APIRouter(tags=["Tweets"])


@router.get("/api/tweets", response_model=TweetListResponse)
async def get_all_tweets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    skip: int | None = Query(None, ge=0),
    author_id: int | None = Query(None, ge=1),
):
    """Followed authors by popularity; author_id optionally selects a public profile."""
    tweets = await get_tweets(
        db, current_user.id, skip if skip is not None else offset, limit, author_id
    )
    return {"result": True, "tweets": [tweet_response(t) for t in tweets]}


@router.post("/api/tweets", response_model=TweetCreatedResponse)
async def create_new_tweet(
    tweet: TweetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Create a tweet atomically with its uploaded images."""
    item = await create_tweet(db, current_user.id, tweet.tweet_data, tweet.tweet_media_ids)
    return {"result": True, "tweet_id": item.id}


@router.delete("/api/tweets/{tweet_id}", response_model=SuccessResponse)
async def delete_tweet_endpoint(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Only the author can delete a tweet."""
    item = await get_tweet_by_id(db, tweet_id)
    if item is None:
        raise HTTPException(404, "Tweet not found")
    if item.author_id != current_user.id:
        raise HTTPException(403, "Only the author can delete this tweet")
    await delete_tweet(db, tweet_id)
    return {"result": True}
