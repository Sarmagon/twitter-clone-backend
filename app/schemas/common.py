"""Shared success and error contracts."""

from typing import Literal

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Successful operation."""

    result: Literal[True] = True


class ErrorResponse(BaseModel):
    """Uniform API error."""

    result: Literal[False] = False
    error_type: str
    error_message: str


ERROR_RESPONSES = {
    code: {"model": ErrorResponse} for code in (400, 401, 403, 404, 409, 413, 415, 422, 500, 503)
}
