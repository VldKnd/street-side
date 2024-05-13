import os
import re
import time
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

def find_and_filter_links(web_page: WebPage) -> Tuple[
        Company,
        Dict[str, DocumentType],
        Dict[str, Document]
    ]:
    home_url = "https://www.nasdaq.com"
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
    time.sleep(1)
    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    links = soup.find_all("a")

    quantative_disclosure_links = [
        link for link in links
        if link.string is not None and "Quantitative Disclosure" in link.string
    ]

    annual_report_links = [
        link for link in links
        if link.string is not None and "Annual Report" in link.string
    ]

    scrapped_company = Company(
        short_name="Nasdaq",
        full_name="Nasdaq's Central Counterparty Clearing House",
        home_url=home_url,
        created_at=None,
        updated_at=None,
    )

    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

    for quantative_disclosure_link in quantative_disclosure_links:
        if quantative_disclosure_link['href'].startswith("http"):
            document_url = quantative_disclosure_link['href']
        else:
            document_url = scrapped_company.home_url + quantative_disclosure_link['href']

        _, extension = os.path.splitext(document_url)
        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="International Organization of Securities Commissions",
            short_name="CPMI-IOSCO",
            is_quaterly=True,
            is_yearly=True,
            created_at=None,
        )

        _, _, Q_quater, year = quantative_disclosure_link.string.split(" ")
        quater = Q_quater.strip("Q")

        try:
            published_day = int(
                os.path.basename(
                os.path.dirname(document_url)
            ))
            published_month = int(
                os.path.basename(
                os.path.dirname(
                os.path.dirname(document_url)
            )))
            published_year = int(
                os.path.basename(
                os.path.dirname(
                os.path.dirname(
                os.path.dirname(document_url)
            ))))
            date_published = datetime(published_year, published_month, published_day)

        except:
            if quater == "4":
                date_published = datetime(int(year)+1, 1, 1)
            elif quater == "3":
                date_published = datetime(int(year), 9, 1)
            elif quater == "2":
                date_published = datetime(int(year), 6, 1)
            else:
                date_published = datetime(int(year), 3, 1)

        scrapped_document = Document(
            document_type_id=scrapped_document_type.hash_id,
            date_published=date_published,
            quater=quater,
            year=year,
            remote_url=document_url,
            extension=extension,
            created_at=None,
        )

        scrapped_document_types[scrapped_document_type.hash_id] = scrapped_document_type
        scrapped_documents[scrapped_document.hash_id] = scrapped_document

    for annual_report_link in annual_report_links:
        if quantative_disclosure_link['href'].startswith("http"):
            document_url = quantative_disclosure_link['href']
        else:
            document_url = scrapped_company.home_url + quantative_disclosure_link['href']
            
        _, extension = os.path.splitext(document_url)

        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="Financial Statement",
            short_name="Financial Statement",
            is_quaterly=False,
            is_yearly=True,
            created_at=None,
        )

        year_regex = re.search(r'\d{4}|$', annual_report_link.string)

        if year_regex is not None:
            year = year_regex.group()
        else:
            year = ""
        
        try:
            published_day = int(
                os.path.basename(
                os.path.dirname(document_url)
            ))
            published_month = int(
                os.path.basename(
                os.path.dirname(
                os.path.dirname(document_url)
            )))
            published_year = int(
                os.path.basename(
                os.path.dirname(
                os.path.dirname(
                os.path.dirname(document_url)
            ))))

            if year == "":
                year = str(published_year - 1)

            date_published = datetime(published_year, published_month, published_day)
        except:
            if year != "":
                date_published = datetime(int(year) + 1, 6, 1)
            else:
                date_published = datetime.now()

        scrapped_document = Document(
            document_type_id=scrapped_document_type.hash_id,
            date_published=date_published,
            year=year,
            remote_url=document_url,
            extension=extension,
            created_at=None,
        )

        scrapped_document_types[scrapped_document_type.hash_id] = scrapped_document_type
        scrapped_documents[scrapped_document.hash_id] = scrapped_document

    return scrapped_company, scrapped_document_types, scrapped_documents