"""Like contracts."""

from pydantic import BaseModel

from app.schemas.common import SuccessResponse


class LikeResponse(SuccessResponse):
    """Operation completed."""


class LikeCreate(BaseModel):
    """Relationship identifiers."""

    tweet_id: int
    user_id: int
