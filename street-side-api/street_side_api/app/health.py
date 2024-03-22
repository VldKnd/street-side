import logging

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/health", tags=["Health"])

class OKStatusResponse(BaseModel):
    status: str = "ok"

@router.get("/")
async def health() -> OKStatusResponse:
    """
    Health check endpoints. Useful for Kubernetes liveness and readiness probes.
    Returns a status code 200 if the API is healthy.

    Returns
    -------
    OKStatusResponse
        Status of the API backends. {"status": "ok"}

    Raises
    ------
    HTTPException
        If the API is not healthy.
    """
    logger.info("Health checking...")
    return OKStatusResponse()
