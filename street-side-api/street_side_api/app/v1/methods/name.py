from logging import getLogger
from typing import Dict

logger = getLogger(__name__)

async def get_name() -> Dict[str, str]:
    """
    Get the name of the project.

    Returns
    -------
    NameResponse
        The name of the project.
    """
    logger.info("Getting the name of the project.")
    return { "name":"Street-Side" }
