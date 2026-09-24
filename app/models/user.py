"""
Модель пользователя (User).

Хранит информацию о пользователях сервиса микроблогов.
Поскольку это корпоративная сеть, регистрация не реализована —
пользователи создаются администратором и получают api_key для авторизации.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    Модель пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя (первичный ключ).
        username (str): Имя пользователя (логин). Должно быть уникальным.
        hashed_password (str): Хэшированный пароль пользователя.
        api_key (str): Уникальный ключ для авторизации через заголовок api-key.
        name (str): Отображаемое имя пользователя.
        nickname (str): Никнейм пользователя (например, @username).
        description (str): Краткое описание профиля (био).
        website (str): Ссылка на сайт пользователя.
        pic (str): URL или путь к аватару пользователя.

    Связи:
        tweets: Список твитов, созданных пользователем.
        likes: Список лайков, поставленных пользователем.
    """

    __tablename__ = "users"  # Имя таблицы в базе данных

    # Основные поля
    id = Column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор")
    username = Column(
        String, unique=True, index=True, nullable=False, comment="Имя пользователя (логин)"
    )
    hashed_password = Column(String, nullable=False, comment="Хэшированный пароль")
    api_key = Column(String, unique=True, index=True, nullable=False, comment="Ключ авторизации")

    # Поля профиля
    name = Column(String, default="", comment="Отображаемое имя")
    nickname = Column(String, default="", comment="Никнейм")
    description = Column(String, default="", comment="Описание профиля")
    website = Column(String, default="", comment="Ссылка на сайт")
    pic = Column(String, default="", comment="URL аватара")

    # Связи с другими таблицами
    # back_populates указывает на обратную связь в связанной модели
    tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Строковое представление объекта для отладки."""
        return f"<User(id={self.id}, username={self.username})>"
