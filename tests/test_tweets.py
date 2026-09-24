"""
Тесты для эндпоинтов твитов.

Тестирует следующие эндпоинты:
- GET /api/tweets - получение ленты твитов
- POST /api/tweets - создание нового твита
- DELETE /api/tweets/{tweet_id} - удаление твита
"""

import pytest


@pytest.mark.asyncio
async def test_get_tweets(client, test_tweet, test_user):
    """
    Тест получения ленты твитов.

    Проверяет:
    - Статус код 200
    - Возвращается результат true
    - Возвращается список твитов
    """
    response = await client.get(
        f"/api/tweets?author_id={test_user.id}", headers={"api-key": test_user.api_key}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweets" in data
    assert len(data["tweets"]) > 0


@pytest.mark.asyncio
async def test_get_tweets_with_pagination(client, test_tweet, test_user):
    """
    Тест получения ленты твитов с пагинацией.

    Проверяет:
    - Статус код 200
    - Возвращается результат true
    - Возвращается список твитов с учетом пагинации
    """
    response = await client.get(
        f"/api/tweets?skip=0&limit=10&author_id={test_user.id}",
        headers={"api-key": test_user.api_key},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweets" in data


@pytest.mark.asyncio
async def test_create_tweet(client, test_user):
    """
    Тест создания нового твита.

    Проверяет:
    - Статус код 200
    - Возвращается информация о созданном твите
    """
    headers = {"api-key": test_user.api_key}
    tweet_data = {"tweet_data": "Test tweet content", "tweet_media_ids": []}
    response = await client.post("/api/tweets", json=tweet_data, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert isinstance(data["tweet_id"], int)


@pytest.mark.asyncio
async def test_create_tweet_invalid_api_key(client):
    """
    Тест создания твита с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    tweet_data = {"tweet_data": "Test tweet content", "tweet_media_ids": []}
    response = await client.post("/api/tweets", json=tweet_data, headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_tweet(client, test_user, test_tweet):
    """
    Тест удаления твита.

    Проверяет:
    - Статус код 200
    - Возвращается результат "true"
    """
    headers = {"api-key": test_user.api_key}
    response = await client.delete(f"/api/tweets/{test_tweet.id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


@pytest.mark.asyncio
async def test_delete_tweet_not_author(client, test_user_2, test_tweet):
    """
    Тест удаления твита не автором.

    Проверяет:
    - Статус код 403 (Forbidden)
    """
    headers = {"api-key": test_user_2.api_key}
    response = await client.delete(f"/api/tweets/{test_tweet.id}", headers=headers)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_tweet_invalid_api_key(client, test_tweet):
    """
    Тест удаления твита с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    response = await client.delete(f"/api/tweets/{test_tweet.id}", headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_tweet_not_found(client, test_user):
    """
    Тест удаления несуществующего твита.

    Проверяет:
    - Статус код 403 (Forbidden) или 404 (Not Found)
    """
    headers = {"api-key": test_user.api_key}
    response = await client.delete("/api/tweets/99999", headers=headers)

    assert response.status_code == 404
