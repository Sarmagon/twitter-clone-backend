"""
Модель подписки (Follow).

Хранит информацию о том, какой пользователь подписан на какого другого пользователя.
Это таблица-связка между пользователями (многие ко многим).
"""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Follow(Base):
    """
    Модель подписки (фолловинга).

    Атрибуты:
        id (int): Уникальный идентификатор подписки (первичный ключ).
        follower_id (int): ID пользователя, который подписался.
        following_id (int): ID пользователя, на которого подписались.

    Связи:
        follower: Объект пользователя, который подписался.
        following: Объект пользователя, на которого подписались.
    """

    __tablename__ = "follows"  # Имя таблицы в базе данных
    __table_args__ = (UniqueConstraint("follower_id", "following_id", name="uq_follows_pair"),)

    # Основные поля
    id = Column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор подписки")
    follower_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ID подписчика"
    )
    following_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя, на которого подписались",
    )

    # Связи с другими таблицами
    # foreign_keys нужен, потому что обе ссылки ведут на одну таблицу users
    follower = relationship("User", foreign_keys=[follower_id], backref="following")
    following = relationship("User", foreign_keys=[following_id], backref="followers")

    def __repr__(self):
        """Строковое представление объекта для отладки."""
        return f"<Follow(follower_id={self.follower_id}, following_id={self.following_id})>"
