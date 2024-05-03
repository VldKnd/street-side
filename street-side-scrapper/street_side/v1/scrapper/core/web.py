
import asyncio
from logging import getLogger
from typing import Callable, Dict, Tuple

from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage
from street_side.v1.storage.document_storage import DocumentStorage

import street_side.v1.scrapper.websites.bme
import street_side.v1.scrapper.websites.cboe
import street_side.v1.scrapper.websites.ccpa
import street_side.v1.scrapper.websites.cme_group
import street_side.v1.scrapper.websites.ecc
import street_side.v1.scrapper.websites.eurex
import street_side.v1.scrapper.websites.ice_credit
import street_side.v1.scrapper.websites.ice_eu
import street_side.v1.scrapper.websites.ice_us
import street_side.v1.scrapper.websites.kdpw
import street_side.v1.scrapper.websites.lch_ltd
import street_side.v1.scrapper.websites.lch_sa
import street_side.v1.scrapper.websites.lme
import street_side.v1.scrapper.websites.nasdaq

logger = getLogger(__name__)

COMPANY_NAME_TO_SCRAPPER_FUNCTION: Dict[
    str,
    Callable[
        [WebPage],
        Tuple[Company, Dict[str, DocumentType], Dict[str, Document]]]
    ] = {
    "lch(sa)": street_side.v1.scrapper.websites.lch_sa.find_and_filter_links,
    "lch(ltd)": street_side.v1.scrapper.websites.lch_ltd.find_and_filter_links,
    "ecc": street_side.v1.scrapper.websites.ecc.find_and_filter_links,
    "nasdaq": street_side.v1.scrapper.websites.nasdaq.find_and_filter_links,
    "cboe": street_side.v1.scrapper.websites.cboe.find_and_filter_links,
    "eurex": street_side.v1.scrapper.websites.eurex.find_and_filter_links,
    "kdpw": street_side.v1.scrapper.websites.kdpw.find_and_filter_links,
    "cme group": street_side.v1.scrapper.websites.cme_group.find_and_filter_links,
    "ccpa": street_side.v1.scrapper.websites.ccpa.find_and_filter_links,
    "lme": street_side.v1.scrapper.websites.lme.find_and_filter_links,
    "bme": street_side.v1.scrapper.websites.bme.find_and_filter_links,
    "ice(us)": street_side.v1.scrapper.websites.ice_us.find_and_filter_links,
    "ice(eu)": street_side.v1.scrapper.websites.ice_eu.find_and_filter_links,
    "ice(credit)": street_side.v1.scrapper.websites.ice_credit.find_and_filter_links
}

def scrape_and_download_data(webpage: WebPage, storage: DocumentStorage):
    scrapper_function = COMPANY_NAME_TO_SCRAPPER_FUNCTION.get(
        webpage.company_name.lower(),
        None,
    )

    if scrapper_function is None:
        logger.error(f"No scrapper function defined for {webpage.company_name}")
        return
    
    try:
        logger.warning(f"Starting to scrape {webpage}!")
        company, scrapped_document_types, scrapped_documents = scrapper_function(webpage)
    except Exception:
        logger.error(f"\nScrapping of {webpage} failed.", exc_info=True)
    else:
        logger.warning(f"Website {webpage} scrapped, downloading data.")
        
        storage.insert_and_download_scrapping_result(
            company=company,
            document_types=scrapped_document_types,\
            documents=scrapped_documents,
        )