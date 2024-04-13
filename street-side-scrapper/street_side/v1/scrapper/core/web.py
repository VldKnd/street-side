import os
import zipfile
from email.policy import default
from logging import getLogger, root
from typing import Callable, Dict, List

import requests
from street_side.v1.data_models.document import RemoteDocument
from street_side.v1.data_models.web import WebPage
from street_side.v1.storage.disk_storage import DiskStorage

from street_side.v1.scrapper.websites.ecc import find_and_filter_links
from street_side.v1.scrapper.websites.utils import download_file

logger = getLogger(__name__)

COMPANY_NAME_TO_SCRAPPER_FUNCTION: Dict[str, Callable[[WebPage], List[RemoteDocument]]] = {
    "ecc": find_and_filter_links,
}

def scrape_and_download_data(webpage: WebPage, workdir: str):
    scrapper_function = COMPANY_NAME_TO_SCRAPPER_FUNCTION.get(
        webpage.company_name.lower(),
        None,
    )

    if scrapper_function is None:
        logger.error(f"No scrapper function defined for {webpage.company_name}")
        return
    
    filtered_scrapped_documents = scrapper_function(webpage)
    disk_storage = DiskStorage(absolute_path_to_root=workdir)
    
    for scrapped_document in filtered_scrapped_documents:
        disk_storage.put(scrapped_document)