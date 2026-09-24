"""
Тесты для эндпоинтов медиа.

Тестирует следующие эндпоинты:
- POST /api/medias - загрузка медиафайла
"""

from io import BytesIO

import pytest
from PIL import Image


def image_bytes():
    data = BytesIO()
    Image.new("RGB", (2, 2), "red").save(data, format="PNG")
    return data.getvalue()


@pytest.mark.asyncio
async def test_upload_media(client, test_user):
    """
    Тест загрузки медиафайла.

    Проверяет:
    - Статус код 200
    - Возвращается результат true
    - Возвращается media_id
    """
    headers = {"api-key": test_user.api_key}
    file_content = image_bytes()
    files = {"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    response = await client.post("/api/medias", files=files, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "media_id" in data


@pytest.mark.asyncio
async def test_upload_media_invalid_api_key(client):
    """
    Тест загрузки медиа с невалидным api-key.

    Проверяет:
    - Статус код 401 (Unauthorized)
    """
    headers = {"api-key": "invalid_key"}
    file_content = image_bytes()
    files = {"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    response = await client.post("/api/medias", files=files, headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_media_no_file(client, test_user):
    """
    Тест загрузки медиа без файла.

    Проверяет:
    - Статус код 422 (Unprocessable Entity)
    """
    headers = {"api-key": test_user.api_key}
    response = await client.post("/api/medias", headers=headers)

    assert response.status_code == 422
