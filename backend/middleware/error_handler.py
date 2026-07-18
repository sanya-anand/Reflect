"""Global exception handlers for the FastAPI application."""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("reflect")


async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return a clean 500 response."""
    logger.error(f"Unhandled error on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Standardize HTTP exception responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
