"""
Тесты для эндпоинтов лайков.

Тестирует следующие эндпоинты:
- POST /api/tweets/{tweet_id}/likes - поставить лайк
- DELETE /api/tweets/{tweet_id}/likes - убрать лайк
"""

import pytest


@pytest.mark.asyncio
async def test_like_tweet(client, test_user, test_tweet):
    """
    Тест постановки лайка на твит.

    Проверяет:
    - Статус код 200
    - Возвращается результат "true"
    """
    headers = {"api-key": test_user.api_key}
    response = await client.post(f"/api/tweets/{test_tweet.id}/likes", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


@pytest.mark.asyncio
async def test_unlike_tweet(client, test_user, test_tweet, session):
    """
    Тест удаления лайка с твита.

    Проверяет:
    - Статус код 200
    - Возвращается результат "true"
    """
    # Сначала ставим лайк
    from app.models import Like

    like = Like(user_id=test_user.id, tweet_id=test_tweet.id)
    session.add(like)
    await session.commit()

    headers = {"api-key": test_user.api_key}
    response = await client.delete(f"/api/tweets/{test_tweet.id}/likes", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


@pytest.mark.asyncio
async def test_like_tweet_invalid_api_key(client, test_tweet):
    """
    Тест постановки лайка с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    response = await client.post(f"/api/tweets/{test_tweet.id}/likes", headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unlike_tweet_invalid_api_key(client, test_tweet):
    """
    Тест удаления лайка с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    response = await client.delete(f"/api/tweets/{test_tweet.id}/likes", headers=headers)

    assert response.status_code == 401
