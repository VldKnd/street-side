
from logging import getLogger
from typing import List

from street_side.v1.storage.disk_storage import DiskStorage

logger = getLogger(__name__)

DISK_STORAGE = DiskStorage()

async def get_all_companies() -> List[str]:
    """
    Get the name of the project.

    Returns
    -------
    NameResponse
        The name of the project.
    """
    return DISK_STORAGE.list_companies()

async def get_documents_names(company_name: str) -> List[str]:
    return DISK_STORAGE.list_company_documents_names(company_name)
