"""
Модель твита (Tweet).

Хранит информацию о твитах — коротких сообщениях пользователей.
Каждый твит привязан к автору (пользователю) и может содержать медиафайлы.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Tweet(Base):
    """
    Модель твита.

    Атрибуты:
        id (int): Уникальный идентификатор твита (первичный ключ).
        content (str): Текстовое содержимое твита.
        author_id (int): ID автора твита (внешний ключ на таблицу users).
        created_at (datetime): Дата и время создания твита.
                               Автоматически устанавливается сервером.

    Связи:
        author: Объект пользователя, создавшего твит.
        likes: Список лайков этого твита.
        medias: Список медиафайлов, прикрепленных к твиту.
    """

    __tablename__ = "tweets"  # Имя таблицы в базе данных

    # Основные поля
    id = Column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор твита")
    content = Column(String, nullable=False, comment="Текст твита")
    author_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID автора твита",
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), comment="Дата и время создания"
    )

    # Связи с другими таблицами
    author = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")
    medias = relationship("Media", back_populates="tweet", cascade="all, delete-orphan")

    def __repr__(self):
        """Строковое представление объекта для отладки."""
        return f"<Tweet(id={self.id}, author_id={self.author_id})>"
