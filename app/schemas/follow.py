"""Follow contracts."""

from pydantic import BaseModel

from app.schemas.common import SuccessResponse


class FollowResponse(SuccessResponse):
    """Operation completed."""


class FollowCreate(BaseModel):
    """Relationship identifiers."""

    follower_id: int
    following_id: int
