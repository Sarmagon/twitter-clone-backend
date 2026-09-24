"""Маршруты для получения профилей пользователей."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user_by_id
from app.database import get_session
from app.dependencies import get_current_user
from app.models.follow import Follow
from app.models.user import User
from app.schemas.user import UserMeResponse

router = APIRouter()


async def build_user_response(db: AsyncSession, user: User) -> dict:
    """Сформировать профиль со списками подписчиков и подписок."""
    followers_result = await db.execute(
        select(User.id, User.name)
        .join(Follow, Follow.follower_id == User.id)
        .where(Follow.following_id == user.id)
        .distinct()
        .order_by(User.id)
    )
    followers = [{"id": user_id, "name": name or ""} for user_id, name in followers_result.all()]

    following_result = await db.execute(
        select(User.id, User.name)
        .join(Follow, Follow.following_id == User.id)
        .where(Follow.follower_id == user.id)
        .distinct()
        .order_by(User.id)
    )
    following = [{"id": user_id, "name": name or ""} for user_id, name in following_result.all()]

    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name or "",
            "profile": {
                "name": user.name or "",
                "nickname": user.nickname or "",
                "description": user.description or "",
                "website": user.website or "",
                "pic": user.pic or "",
            },
            "account": {"followingCount": len(following), "followerCount": len(followers)},
            "followers": followers,
            "following": following,
        },
    }


@router.get("/api/users/me", response_model=UserMeResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Получить профиль текущего пользователя по api-key."""
    return await build_user_response(db, current_user)


@router.get("/api/users/{user_id}", response_model=UserMeResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Получить профиль пользователя по ID."""
    user = await get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return await build_user_response(db, user)
