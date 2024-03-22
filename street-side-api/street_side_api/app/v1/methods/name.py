from logging import getLogger

import street_side_data_models.v1.name

logger = getLogger(__name__)

async def get_name() -> street_side_data_models.v1.name.Name:
    """
    Get the name of the project.

    Returns
    -------
    NameResponse
        The name of the project.
    """
    logger.info("Getting the name of the project.")
    return street_side_data_models.v1.name.Name(name="Street Side")
