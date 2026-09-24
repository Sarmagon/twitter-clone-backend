"""
Модель лайка (Like).

Хранит информацию о том, какой пользователь лайкнул какой твит.
Это таблица-связка между пользователями и твитами (многие ко многим).
"""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Like(Base):
    """
    Модель лайка.

    Атрибуты:
        id (int): Уникальный идентификатор лайка (первичный ключ).
        user_id (int): ID пользователя, поставившего лайк.
        tweet_id (int): ID твита, который был лайкнут.

    Связи:
        user: Объект пользователя, поставившего лайк.
        tweet: Объект твита, который был лайкнут.
    """

    __tablename__ = "likes"  # Имя таблицы в базе данных
    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="uq_likes_pair"),)

    # Основные поля
    id = Column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор лайка")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя",
    )
    tweet_id = Column(
        Integer, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False, comment="ID твита"
    )

    # Связи с другими таблицами
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")

    def __repr__(self):
        """Строковое представление объекта для отладки."""
        return f"<Like(user_id={self.user_id}, tweet_id={self.tweet_id})>"
