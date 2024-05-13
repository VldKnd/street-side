import os
import re
from datetime import datetime
from logging import getLogger
from typing import Dict, Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage

from street_side.v1.scrapper.websites.utils import set_chrome_options

logger = getLogger(__name__)

def iosco_filter(link) -> bool:
    for content in link.contents:
        try:
            elements_text = content.get_text()
            if (
                "IOSCO" in elements_text
                and
                "CPMI" in elements_text
            ):
                return True
        except:
            continue
    return False

def pfmi_filter(link) -> bool:
    for content in link.contents:
        try:
            elements_text = content.get_text()
            if (
                "IOSCO" in elements_text
                and
                "CPMI" in elements_text
                and
                "Document" in elements_text
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
    driver.quit()
    home_url = "https://www.lme.com"
    
    scrapped_company = Company(
        short_name="LME",
        full_name="London Metal Exchange",
        home_url=home_url,
        created_at=None,
        updated_at=None
    )

    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all("a")
    archive_links = filter(iosco_filter, links)
    pfmi_links = filter(pfmi_filter, links)

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

    for pfmi_link in pfmi_links:
        if pfmi_link['href'].startswith("http"):
            document_url = pfmi_link['href']
        else:
            document_url = scrapped_company.home_url + pfmi_link['href']
        _, extension = os.path.splitext(document_url)

        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="Principles for financial market infrastructures",
            short_name="PFMI",
            is_quaterly=False,
            is_yearly=True,
            created_at=None,
        )

        year_regex = re.search(r'\d{4}|$', pfmi_link.get_text())

        if year_regex is not None:
            year = year_regex.group()
            if year == "":
                continue
            published_date = datetime(int(year), 12, 1)
    
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
