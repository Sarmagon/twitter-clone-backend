"""
Тесты для эндпоинтов пользователей.

Тестирует следующие эндпоинты:
- GET /api/users/me - получение информации о текущем пользователе
- GET /api/users/{user_id} - получение информации о пользователе по ID
- POST /api/users/{user_id}/follow - подписка на пользователя
- DELETE /api/users/{user_id}/follow - отписка от пользователя
"""

import pytest


@pytest.mark.asyncio
async def test_get_current_user(client, test_user):
    """
    Тест получения информации о текущем пользователе.

    Проверяет:
    - Статус код 200
    - Возвращается результат "true"
    - Возвращается информация о пользователе
    """
    headers = {"api-key": test_user.api_key}
    response = await client.get("/api/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "user" in data
    assert data["user"]["id"] == test_user.id


@pytest.mark.asyncio
async def test_get_current_user_invalid_api_key(client):
    """
    Тест получения информации о пользователе с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    response = await client.get("/api/users/me", headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_user_by_id(client, test_user):
    """
    Тест получения информации о пользователе по ID.
    """
    response = await client.get(
        f"/api/users/{test_user.id}", headers={"api-key": test_user.api_key}
    )

    assert response.status_code == 200
    data = response.json()
    # Проверяем, что вернулся правильный ID пользователя
    assert data["user"]["id"] == test_user.id


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client, test_user):
    """
    Тест получения информации о несуществующем пользователе.

    Проверяет:
    - Статус код 404 (Not Found)
    """
    response = await client.get("/api/users/99999", headers={"api-key": test_user.api_key})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_follow_user(client, test_user, test_user_2):
    """
    Тест подписки на пользователя.
    """
    headers = {"api-key": test_user.api_key}
    response = await client.post(f"/api/users/{test_user_2.id}/follow", headers=headers)

    assert response.status_code == 200
    data = response.json()
    # Эндпоинт подписки возвращает {"result": "true"}
    assert data["result"] is True


@pytest.mark.asyncio
async def test_unfollow_user(client, test_user, test_user_2, session):
    """
    Тест отписки от пользователя.

    Проверяет:
    - Статус код 200
    - Возвращается результат "true"
    """
    # Сначала подписываемся
    from app.models import Follow

    follow = Follow(follower_id=test_user.id, following_id=test_user_2.id)
    session.add(follow)
    await session.commit()

    headers = {"api-key": test_user.api_key}
    response = await client.delete(f"/api/users/{test_user_2.id}/follow", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


@pytest.mark.asyncio
async def test_follow_user_invalid_api_key(client, test_user_2):
    """
    Тест подписки с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    response = await client.post(f"/api/users/{test_user_2.id}/follow", headers=headers)

    assert response.status_code == 401
