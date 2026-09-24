"""
Роутер для управления подписками.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.follows import create_follow, delete_follow
from app.crud.users import get_user_by_id
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.follow import FollowResponse

router = APIRouter()


@router.post("/api/users/{user_id}/follow", response_model=FollowResponse)
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Подписаться на пользователя.
    """
    if user_id == current_user.id:
        raise HTTPException(400, "Cannot follow yourself")
    user_to_follow = await get_user_by_id(db, user_id)
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")

    await create_follow(db, follower_id=current_user.id, following_id=user_id)
    return {"result": True}


@router.delete("/api/users/{user_id}/follow", response_model=FollowResponse)
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Отписаться от пользователя.
    """
    await delete_follow(db, follower_id=current_user.id, following_id=user_id)
    return {"result": True}
