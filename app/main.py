"""Application, documented errors and health probe."""

import logging

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import configure_mappers
from starlette.exceptions import HTTPException

from app.config import settings
from app.database import get_session
from app.routers import follows, likes, media, tweets, users
from app.schemas.common import ERROR_RESPONSES

configure_mappers()
app = FastAPI(
    title="Twitter Clone API",
    version="1.1.0",
    description="Corporate microblog service. All /api endpoints require api-key.",
    responses=ERROR_RESPONSES,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


def error_response(status: int, kind: str, message: str) -> JSONResponse:
    """Use the assignment's error envelope."""
    return JSONResponse(
        status_code=status, content={"result": False, "error_type": kind, "error_message": message}
    )


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    """Expected client error."""
    return error_response(exc.status_code, f"HTTP{exc.status_code}", str(exc.detail))


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    """Describe invalid fields without echoing secret request values."""
    message = "; ".join(".".join(str(p) for p in e["loc"]) + ": " + e["msg"] for e in exc.errors())
    return error_response(422, "ValidationError", message)


@app.exception_handler(IntegrityError)
async def conflict_error(request: Request, exc: IntegrityError):
    """Handle races with deletion or conflicting relationships."""
    return error_response(409, "Conflict", "The operation conflicts with current data")


@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception):
    """Log details server-side only."""
    logging.getLogger(__name__).error("Unhandled request failure", exc_info=exc)
    return error_response(500, "InternalError", "Unexpected server error")


for router in (users.router, tweets.router, media.router, likes.router, follows.router):
    app.include_router(router)
settings.MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")


@app.get("/")
async def root():
    """Service identity."""
    return {"message": "Twitter Clone API"}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_session)):
    """Check database connectivity as well as the web process."""
    try:
        await db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return error_response(503, "DatabaseUnavailable", "Database is not ready")
    return {"status": "ok"}
