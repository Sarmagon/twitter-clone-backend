"""
Тесты для эндпоинтов подписок.

Тестирует следующие эндпоинты:
- POST /api/users/{user_id}/follow - подписка на пользователя
- DELETE /api/users/{user_id}/follow - отписка от пользователя

Примечание: Основные тесты подписок уже находятся в test_users.py.
Этот файл содержит дополнительные тесты для edge cases.
"""

import pytest


@pytest.mark.asyncio
async def test_follow_self(client, test_user):
    """
    Тест подписки на самого себя.

    Проверяет:
    - Статус код 200 (или 400, если есть валидация)
    """
    headers = {"api-key": test_user.api_key}
    response = await client.post(f"/api/users/{test_user.id}/follow", headers=headers)

    # В зависимости от реализации, может быть 200 или 400
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_follow_nonexistent_user(client, test_user):
    """
    Тест подписки на несуществующего пользователя.

    Проверяет:
    - Статус код 404 (Not Found) или 500 (Internal Server Error)
    """
    headers = {"api-key": test_user.api_key}
    response = await client.post("/api/users/99999/follow", headers=headers)

    # В зависимости от реализации, может быть 404 или 500
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unfollow_nonexistent_user(client, test_user):
    """
    Тест отписки от несуществующего пользователя.

    Проверяет:
    - Статус код 404 (Not Found) или 200 (если отписка без проверки)
    """
    headers = {"api-key": test_user.api_key}
    response = await client.delete("/api/users/99999/follow", headers=headers)

    # В зависимости от реализации, может быть 404 или 200
    assert response.status_code in [200, 404]
