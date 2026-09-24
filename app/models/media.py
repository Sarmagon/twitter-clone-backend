"""
Модель медиафайла (Media).

Хранит информацию о загруженных файлах (изображениях),
которые могут быть прикреплены к твитам.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Media(Base):
    """
    Модель медиафайла.

    Атрибуты:
        id (int): Уникальный идентификатор медиафайла (первичный ключ).
        file_path (str): Путь к файлу на сервере или URL.
        tweet_id (int | None): ID твита, к которому прикреплен файл.
                               Может быть NULL, если файл загружен, но твит еще не создан.

    Связи:
        tweet: Объект твита, к которому прикреплен файл.
    """

    __tablename__ = "medias"  # Имя таблицы в базе данных

    # Основные поля
    id = Column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор медиа")
    file_path = Column(String, nullable=False, comment="Путь к файлу")
    tweet_id = Column(
        Integer,
        ForeignKey("tweets.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID твита (может быть NULL)",
    )

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Связи с другими таблицами
    tweet = relationship("Tweet", back_populates="medias")

    def __repr__(self):
        """Строковое представление объекта для отладки."""
        return f"<Media(id={self.id}, tweet_id={self.tweet_id})>"
