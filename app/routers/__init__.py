from app.routers.follows import router as follows_router
from app.routers.likes import router as likes_router
from app.routers.media import router as media_router
from app.routers.tweets import router as tweets_router
from app.routers.users import router as users_router

__all__ = [
    "users_router",
    "tweets_router",
    "media_router",
    "likes_router",
    "follows_router",
]
