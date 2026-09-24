"""Regression tests for assignment behavior missing from the original suite."""

from io import BytesIO

import pytest
from PIL import Image
from sqlalchemy import func, select

from app.models import Follow, Like, Tweet


def image_bytes():
    stream = BytesIO()
    Image.new("RGB", (4, 4), "blue").save(stream, format="PNG")
    return stream.getvalue()


async def test_follow_profile_roundtrip(client, test_user, test_user_2, session):
    headers = {"api-key": test_user.api_key}
    url = f"/api/users/{test_user_2.id}/follow"
    for _ in range(2):
        assert (await client.post(url, headers=headers)).json() == {"result": True}
    assert await session.scalar(select(func.count()).select_from(Follow)) == 1
    profile = (await client.get(f"/api/users/{test_user_2.id}", headers=headers)).json()["user"]
    assert profile["followers"] == [{"id": test_user.id, "name": test_user.name}]
    me = (await client.get("/api/users/me", headers=headers)).json()["user"]
    assert me["following"] == [{"id": test_user_2.id, "name": test_user_2.name}]
    for _ in range(2):
        assert (await client.delete(url, headers=headers)).status_code == 200
    assert await session.scalar(select(func.count()).select_from(Follow)) == 0


async def test_feed_filter_ranking_pagination(client, test_user, test_user_2, session):
    own = Tweet(author_id=test_user.id, content="own")
    popular = Tweet(author_id=test_user_2.id, content="popular")
    other = Tweet(author_id=test_user_2.id, content="other")
    session.add_all([own, popular, other])
    await session.flush()
    session.add_all(
        [
            Follow(follower_id=test_user.id, following_id=test_user_2.id),
            Like(user_id=test_user.id, tweet_id=popular.id),
        ]
    )
    await session.commit()
    headers = {"api-key": test_user.api_key}
    data = (await client.get("/api/tweets", headers=headers)).json()
    assert [t["id"] for t in data["tweets"]] == [popular.id, other.id]
    assert data["tweets"][0]["likes"] == [{"user_id": test_user.id, "name": test_user.name}]
    data = (await client.get("/api/tweets?offset=1&limit=1", headers=headers)).json()
    assert [t["id"] for t in data["tweets"]] == [other.id]
    assert (await client.get("/api/tweets?limit=-1", headers=headers)).status_code == 422


async def test_empty_feed_without_follows(client, test_user, test_tweet):
    response = await client.get("/api/tweets", headers={"api-key": test_user.api_key})
    assert response.json() == {"result": True, "tweets": []}


async def test_like_duplicate_and_missing(client, test_user, test_tweet, session):
    headers = {"api-key": test_user.api_key}
    url = f"/api/tweets/{test_tweet.id}/likes"
    for _ in range(2):
        assert (await client.post(url, headers=headers)).json() == {"result": True}
    assert await session.scalar(select(func.count()).select_from(Like)) == 1
    assert (await client.post("/api/tweets/99999/likes", headers=headers)).status_code == 404


async def test_media_ownership_atomicity_and_attachment(client, test_user, test_user_2, session):
    headers = {"api-key": test_user.api_key}
    upload = await client.post(
        "/api/medias", headers=headers, files={"file": ("pic.png", image_bytes(), "image/png")}
    )
    assert upload.status_code == 200
    media_id = upload.json()["media_id"]
    payload = {"tweet_data": "with image", "tweet_media_ids": [media_id]}
    forbidden = await client.post(
        "/api/tweets", headers={"api-key": test_user_2.api_key}, json=payload
    )
    assert forbidden.status_code == 403
    assert await session.scalar(select(func.count()).select_from(Tweet)) == 0
    created = await client.post("/api/tweets", headers=headers, json=payload)
    assert set(created.json()) == {"result", "tweet_id"}
    listed = (await client.get(f"/api/tweets?author_id={test_user.id}", headers=headers)).json()[
        "tweets"
    ]
    assert listed[0]["attachments"][0].startswith("/static/media/")
    assert (await client.post("/api/tweets", headers=headers, json=payload)).status_code == 409
    assert await session.scalar(select(func.count()).select_from(Tweet)) == 1


@pytest.mark.parametrize(
    "payload",
    [
        {"tweet_data": ""},
        {"tweet_data": "   "},
        {"tweet_data": "hi", "tweet_media_ids": [1, 1]},
        {"tweet_data": "hi", "tweet_media_ids": [-1]},
    ],
)
async def test_invalid_tweet(client, test_user, payload):
    response = await client.post(
        "/api/tweets", headers={"api-key": test_user.api_key}, json=payload
    )
    assert response.status_code == 422
    assert set(response.json()) == {"result", "error_type", "error_message"}


async def test_invalid_image(client, test_user):
    response = await client.post(
        "/api/medias",
        headers={"api-key": test_user.api_key},
        files={"file": ("fake.png", b"not an image", "image/png")},
    )
    assert response.status_code == 415


async def test_missing_media_is_atomic(client, test_user, session):
    response = await client.post(
        "/api/tweets",
        headers={"api-key": test_user.api_key},
        json={"tweet_data": "bad", "tweet_media_ids": [99999]},
    )
    assert response.status_code == 404
    assert await session.scalar(select(func.count()).select_from(Tweet)) == 0


@pytest.mark.parametrize("path", ["/api/tweets", "/api/users/me", "/api/users/1"])
async def test_auth_required(client, path):
    response = await client.get(path)
    assert response.status_code == 401
    assert response.json()["result"] is False


async def test_delete_cascades_likes(client, test_user, test_tweet, session):
    session.add(Like(user_id=test_user.id, tweet_id=test_tweet.id))
    await session.commit()
    response = await client.delete(
        f"/api/tweets/{test_tweet.id}", headers={"api-key": test_user.api_key}
    )
    assert response.json() == {"result": True}
    assert await session.scalar(select(func.count()).select_from(Like)) == 0
