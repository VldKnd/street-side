
from logging import getLogger
from typing import List

from street_side.v1.data_models.configuration import StreetSideConfiguration
from street_side.v1.data_models.web import WebPage
from street_side.v1.storage.disk_storage import DiskStorage

logger = getLogger(__name__)

APPLICATION_CONFIGURATION = StreetSideConfiguration.from_env_json_file()
DISK_STORAGE = DiskStorage(absolute_path_to_root=APPLICATION_CONFIGURATION.datastore_path)

async def get_all_companies() -> List[WebPage]:
    """
    Get the name of the project.

    Returns
    -------
    NameResponse
        The name of the project.
    """
    companies_names = DISK_STORAGE.list_companies_names()
    
    return [
        APPLICATION_CONFIGURATION.scrapper_web_pages[company_name]
        for company_name in companies_names
        if company_name in APPLICATION_CONFIGURATION.scrapper_web_pages
    ] * 10

async def get_documents_names(company_name: str) -> List[str]:
    return DISK_STORAGE.list_company_documents_names(company_name)
