"""Queries for externally provisioned users."""

import hashlib
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Get a user without implicit relationship reads."""
    return await db.scalar(select(User).where(User.id == user_id))


async def get_user_by_api_key(db: AsyncSession, api_key: str) -> User | None:
    """Resolve the corporate API key."""
    return await db.scalar(select(User).where(User.api_key == api_key))


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """List users in stable order."""
    return (await db.scalars(select(User).order_by(User.id).offset(skip).limit(limit))).all()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Provision a user; never store the input password verbatim."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", user.password.encode(), salt.encode(), 600000)
    item = User(
        username=user.username,
        name=user.username,
        api_key=user.api_key,
        hashed_password=f"pbkdf2_sha256$600000${salt}${digest.hex()}",
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
