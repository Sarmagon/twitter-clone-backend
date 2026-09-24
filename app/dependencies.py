"""Corporate API-key authentication."""

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user_by_api_key
from app.database import get_session
from app.models.user import User


async def get_current_user(
    api_key: str | None = Header(None, alias="api-key"),
    db: AsyncSession = Depends(get_session),
) -> User:
    """Require a valid key on every business endpoint."""
    if not api_key:
        raise HTTPException(401, "API key is required")
    user = await get_user_by_api_key(db, api_key)
    if user is None:
        raise HTTPException(401, "Invalid API key")
    return user
