
from logging import getLogger
from typing import Callable, Dict, Tuple

from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage
from street_side.v1.storage.document_storage import DocumentStorage

from street_side.v1.scrapper.websites.ecc import find_and_filter_links

logger = getLogger(__name__)

COMPANY_NAME_TO_SCRAPPER_FUNCTION: Dict[
    str,
    Callable[
        [WebPage],
        Tuple[Company, Dict[str, DocumentType], Dict[str, Document]]]
    ] = {
    "ecc": find_and_filter_links,
}

def scrape_and_download_data(webpage: WebPage, storage: DocumentStorage):
    scrapper_function = COMPANY_NAME_TO_SCRAPPER_FUNCTION.get(
        webpage.company_name.lower(),
        None,
    )

    if scrapper_function is None:
        logger.error(f"No scrapper function defined for {webpage.company_name}")
        return
    
    company, scrapped_document_types, scrapped_documents = scrapper_function(webpage)
    storage.insert_and_download_scrapping_result(
        company=company,
        document_types=scrapped_document_types,\
        documents=scrapped_documents,
    )