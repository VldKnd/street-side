import os
import re
from datetime import datetime
from logging import getLogger
from typing import Dict, Tuple

import bs4
import requests
from bs4 import BeautifulSoup
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage

logger = getLogger(__name__)

def iosco_filter(link) -> bool:
    try:
        elements_text = link['href']
        if (
            (
                "IOSCO" in elements_text
                or
                "Public Quantitative Disclosure" in elements_text
                or
                "PQD" in elements_text
            )
            and
            "FMI" not in elements_text
        ):
            return True
        else:
            return False
    except:
        return False

def pfmi_filter(link) -> bool:
    for content in link.contents:
        try:
            elements_text = content.get_text()
            if (
                "IOSCO" in elements_text
                and
                "FMI" in elements_text
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
    home_url = "https://www.ccpa.at"
    url = web_page.url
    headers = {
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    }
    response = requests.get(
        url=url,
        headers=headers
    )
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all("a")
    iosco_links = filter(iosco_filter, links)
    pfmi_links = filter(pfmi_filter, links)

    scrapped_company = Company(
        short_name="CCPA",
        full_name="Central Counterparty Austria",
        home_url=home_url,
        created_at=None
    )

    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

    for iosco_link in iosco_links:
        if iosco_link['href'].startswith("http"):
            document_url = iosco_link['href']
        else:
            document_url = scrapped_company.home_url + iosco_link['href']
        _, extension = os.path.splitext(document_url)

        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="International Organization of Securities Commissions",
            short_name="CPMI-IOSCO",
            is_quaterly=True,
            is_yearly=True,
            created_at=None,
        )

        links_text = iosco_link['href']
        
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

        extra_information_text = pfmi_link.parent.get_text()

        date_regex = re.search(r'\d{2}/\d{2}/\d{4}', extra_information_text)
        if date_regex is not None:
            date = date_regex.group()
            day, month, year = date.split("/")
            published_date = datetime(int(year) , int(month), int(day))
        else:
            year_regex = re.search(r'\d{4}|$', extra_information_text)
            if year_regex is not None:
                year = year_regex.group()\
                
                if year == "":
                    continue

            published_date = datetime(int(year), 1, 1)

        scrapped_document = Document(
            document_type_id=scrapped_document_type.hash_id,
            date_published=published_date,
            year=year,
            remote_url=document_url,
            extension=extension,
            created_at=None,
        )

        scrapped_document_types[scrapped_document_type.hash_id] = scrapped_document_type
        scrapped_documents[scrapped_document.hash_id] = scrapped_document
    
    return scrapped_company, scrapped_document_types, scrapped_documents