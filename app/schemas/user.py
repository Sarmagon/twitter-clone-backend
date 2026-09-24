"""
Схемы Pydantic для пользователей.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UserProfile(BaseModel):
    """Профиль пользователя"""

    pic: Optional[str] = ""
    nickname: Optional[str] = ""
    name: Optional[str] = ""
    description: Optional[str] = ""
    website: Optional[str] = ""


class UserAccount(BaseModel):
    """Счетчики подписок"""

    followingCount: Optional[int] = 0
    followerCount: Optional[int] = 0


class UserBase(BaseModel):
    """Базовая схема пользователя"""

    username: str
    api_key: str


class UserCreate(UserBase):
    """Схема для создания пользователя"""

    password: str


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя"""

    id: int
    name: str
    profile: Optional[UserProfile] = None
    account: Optional[UserAccount] = None
    followers: Optional[List[dict]] = []
    following: Optional[List[dict]] = []

    # Современный способ настройки в Pydantic V2
    model_config = ConfigDict(from_attributes=True)


class UserMeResponse(BaseModel):
    """Схема ответа для /api/users/me"""

    result: bool = True
    user: UserResponse


class UserEdit(BaseModel):
    """Схема для редактирования профиля"""

    name: Optional[str] = None
    nickname: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    pic: Optional[str] = None
