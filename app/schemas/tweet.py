"""Tweet request and response contracts."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import SuccessResponse


class TweetAuthor(BaseModel):
    """Author visible in a tweet."""

    id: int
    name: str


class TweetLike(BaseModel):
    """User who liked a tweet."""

    user_id: int
    name: str


class TweetCreate(BaseModel):
    """A text tweet with optional uploaded images."""

    tweet_data: str = Field(min_length=1, max_length=10000)
    tweet_media_ids: list[int] = Field(default_factory=list, max_length=10)

    @field_validator("tweet_data")
    @classmethod
    def nonblank(cls, value: str) -> str:
        """Reject blank messages."""
        if not value.strip():
            raise ValueError("Tweet text must not be blank")
        return value

    @field_validator("tweet_media_ids")
    @classmethod
    def valid_ids(cls, value: list[int]) -> list[int]:
        """Reject repeated and nonpositive image IDs."""
        if any(item <= 0 for item in value) or len(set(value)) != len(value):
            raise ValueError("Media IDs must be positive and unique")
        return value


class TweetCreatedResponse(SuccessResponse):
    """ID of the newly created tweet."""

    tweet_id: int


class TweetResponse(BaseModel):
    """Public tweet including attachments and likes."""

    id: int
    content: str
    attachments: list[str] = Field(default_factory=list)
    author: TweetAuthor
    likes: list[TweetLike] = Field(default_factory=list)
    created_at: datetime | None = None


class TweetListResponse(SuccessResponse):
    """Paginated feed."""

    tweets: list[TweetResponse]


class TweetEdit(BaseModel):
    """Reserved edit payload."""

    id: int
    content: str
