import time
from logging import getLogger

from fastapi import HTTPException, status
from pydantic import BaseModel

logger = getLogger(__name__)

class OKStatusResponse(BaseModel):
    status: str = "ok"
    seconds: float = 0.0

async def get_sleep(seconds: float) -> OKStatusResponse:
    """
    Retrieve the name of the app.

    Returns
    -------
    Name
        The name of the app.

    Raises
    ------
    HTTPException
        If an unexpected error occurs, raises a 500 internal server error status code.
    """
    try:
        logger.warn(f"Sleeping for {seconds} seconds")
        time.sleep(seconds)
    except Exception as e:
        logger.exception(f"Error waiting", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return OKStatusResponse(
            status="ok",
            seconds=seconds
        )