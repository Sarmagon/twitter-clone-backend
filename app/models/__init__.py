"""
Инициализация пакета моделей.

Импортирует все модели, чтобы Alembic мог их обнаружить
при создании миграций базы данных.
"""

from app.models.follow import Follow
from app.models.like import Like
from app.models.media import Media
from app.models.tweet import Tweet
from app.models.user import User

# Список всех моделей для экспорта
__all__ = [
    "User",
    "Tweet",
    "Media",
    "Like",
    "Follow",
]
