"""
Фикстуры для тестов.

Этот файл содержит общие настройки и фикстуры,
которые используются во всех тестах приложения.
"""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.database import Base, get_session
from app.main import app
from app.models import Media, Tweet, User

# URL тестовой базы данных (SQLite в памяти для быстрых тестов)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    """Бэкенд для anyio (используется asyncio)."""
    return "asyncio"


@pytest_asyncio.fixture(scope="function")
async def engine():
    """Создает тестовый движок базы данных."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    @event.listens_for(engine.sync_engine, "connect")
    def enable_foreign_keys(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    """Создает тестовую сессию базы данных."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session):
    """Создает тестовый клиент FastAPI."""

    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(session):
    """Создает тестового пользователя."""
    user = User(
        username="test_user",
        hashed_password="hashed_password",
        api_key="test_api_key",
        name="Test User",
        nickname="@test_user",
        description="Test description",
        website="https://test.com",
        pic="https://test.com/pic.jpg",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_user_2(session):
    """Создает второго тестового пользователя."""
    user = User(
        username="test_user_2",
        hashed_password="hashed_password_2",
        api_key="test_api_key_2",
        name="Test User 2",
        nickname="@test_user_2",
        description="Test description 2",
        website="https://test2.com",
        pic="https://test2.com/pic.jpg",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_tweet(session, test_user):
    """Создает тестовый твит."""
    tweet = Tweet(content="Test tweet content", author_id=test_user.id)
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return tweet


@pytest_asyncio.fixture(scope="function")
async def test_media(session):
    """Создает тестовое медиа."""
    media = Media(file_path="static/media/test.jpg")
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media


@pytest.fixture(autouse=True)
def upload_directory(tmp_path, monkeypatch):
    """Keep test uploads out of user files."""
    monkeypatch.setattr(settings, "MEDIA_DIR", tmp_path / "media")
