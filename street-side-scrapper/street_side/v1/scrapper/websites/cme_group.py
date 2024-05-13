import os
import re
from datetime import datetime
from logging import getLogger
from typing import Dict, Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage

from street_side.v1.scrapper.websites.utils import set_chrome_options

logger = getLogger(__name__)

def archive_filter(link) -> bool:
    for content in link.contents:
        try:
            elements_text = content.get_text()
            if (
                "DataFile" in elements_text
                and
                "CME" in elements_text
            ):
                return True
        except:
            continue
    return False

def find_and_filter_links(web_page: WebPage) -> Tuple[
        Company,
        Dict[str, DocumentType],
        Dict[str, Document]
    ]:
    home_url = "https://www.cmegroup.com"
    url = web_page.url
    chrome_options = set_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all("a")
    archive_links = filter(archive_filter, links)

    scrapped_company = Company(
        short_name="CME",
        full_name="Chicago Mercantile Exchange Group",
        home_url=home_url,
        created_at=None,
        updated_at=None
    )

    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

    for archive_link in archive_links:
        if archive_link['href'].startswith("http"):
            document_url = archive_link['href']
        else:
            document_url = scrapped_company.home_url + archive_link['href']
        _, extension = os.path.splitext(document_url)

        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="Data Archive",
            short_name="Data Archive",
            is_quaterly=True,
            is_yearly=True,
            created_at=None,
        )

        links_text = archive_link.get_text()
        
        year_regex = re.search(r'\d{4}|$', links_text)
        quater_regex = re.search(r'Q\d|$', links_text)

        if year_regex is not None and quater_regex is not None:
            year = year_regex.group()
            Q_quater = quater_regex.group()

            quater = Q_quater.strip("Q")

            if year == "" or quater == "":
                continue

        published_date = datetime(int(year) , ((int(quater) - 1) * 3) + 1, 1)

        scrapped_document = Document(
            document_type_id=scrapped_document_type.hash_id,
            date_published=published_date,
            year=year,
            quater=quater,
            remote_url=document_url,
            extension=extension,
            created_at=None,
        )

        scrapped_document_types[scrapped_document_type.hash_id] = scrapped_document_type
        scrapped_documents[scrapped_document.hash_id] = scrapped_document
    
    return scrapped_company, scrapped_document_types, scrapped_documents


