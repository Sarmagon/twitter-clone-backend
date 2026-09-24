"""
Схемы Pydantic для медиафайлов.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class MediaCreate(BaseModel):
    """Схема для загрузки медиа (используется при загрузке файла)"""

    pass


class MediaResponse(BaseModel):
    """Схема ответа после загрузки медиа"""

    result: bool = True
    media_id: int


class MediaItem(BaseModel):
    """Схема медиа в твите"""

    id: int
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
