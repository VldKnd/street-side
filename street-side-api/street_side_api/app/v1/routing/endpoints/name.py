from logging import getLogger
from fastapi import HTTPException, status
import street_side_data_models.v1
import street_side_api.app.v1.methods.name

logger = getLogger(__name__)

async def get_name() -> street_side_data_models.v1.Name:
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
        response = await street_side_api.app.v1.methods.name.get_name()
    except Exception as e:
        logger.exception(f"Error getting name of the app", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response