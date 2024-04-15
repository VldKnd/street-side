from logging import getLogger
from typing import List

from fastapi import HTTPException, status
from street_side.v1.data_models.web import WebPage

import street_side_api.app.v1.methods.data

logger = getLogger(__name__)

async def get_all_companies() -> List[WebPage]:
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
        response = await street_side_api.app.v1.methods.data.get_all_companies()
    except Exception as e:
        logger.exception(f"Error getting companies from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response
    
async def get_document_names(company_name: str) -> List[str]:
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
        response = await street_side_api.app.v1.methods.data.get_documents_names(company_name)
    except Exception as e:
        logger.exception(f"Error getting companies from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response