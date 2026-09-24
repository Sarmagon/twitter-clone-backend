"""Bounded, verified image uploads."""

import asyncio
import warnings
from io import BytesIO
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud.media import create_media
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.media import MediaResponse

router = APIRouter(tags=["Media"])


def verified_extension(data: bytes) -> str:
    """Check real image contents rather than the client filename or MIME type."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as image:
                extension = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "GIF": ".gif"}.get(
                    image.format
                )
                if extension is None:
                    raise HTTPException(415, "Use JPEG, PNG, WEBP or GIF")
                image.verify()
                return extension
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        raise HTTPException(415, "Invalid or oversized image") from exc


@router.post("/api/medias", response_model=MediaResponse)
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Upload one image up to 5 MiB; return its ID for a later tweet."""
    data = await file.read(settings.MAX_UPLOAD_BYTES + 1)
    if len(data) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Image exceeds the upload limit")
    extension = await asyncio.to_thread(verified_extension, data)
    name = f"{uuid4()}{extension}"
    settings.MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    path = settings.MEDIA_DIR / name
    await asyncio.to_thread(path.write_bytes, data)
    try:
        media = await create_media(db, f"static/media/{name}", current_user.id)
    except Exception:
        await db.rollback()
        await asyncio.to_thread(path.unlink, missing_ok=True)
        raise
    return {"result": True, "media_id": media.id}
