import os
import re
from datetime import date, datetime
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
    for content in link.contents:
        try:
            if (
                "CPMI" in content
                and
                "IOSCO" in content
                and
                "PFMI" not in content
            ):
                return True
        except:
            continue
    return False

def cpmi_pfmi_filter(link) -> bool:
    for content in link.contents:
        try:
            if (
                "CPMI" in content
                and
                "PFMI" in content
            ):
                return True
        except:
            continue

    return False

def cpss_pfmi_filter(link) -> bool:
    for content in link.contents:
        try:
            if (
                "CPSS" in content
                and
                "PFMI" in content
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
    home_url = "https://www.eurex.com"
    url = web_page.url
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    }
    response = requests.get(
        url=url,
        headers=headers,
        timeout=10
    )
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    links = soup.find_all("a")
    iosco_links = filter(iosco_filter, links)
    cpmi_pfmi_links = filter(cpmi_pfmi_filter, links)
    cpss_pfmi_links = filter(cpss_pfmi_filter, links)

    scrapped_company = Company(
        short_name="Eurex",
        full_name="Eurex Clearing",
        home_url=home_url,
        created_at=None,
        updated_at=None
    )

    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

    for cpss_pfmi_link in cpss_pfmi_links:
        if cpss_pfmi_link['href'].startswith("http"):
            document_url = cpss_pfmi_link['href']
        else:
            document_url = scrapped_company.home_url + cpss_pfmi_link['href']
        _, extension = os.path.splitext(document_url)

        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="Principles for financial market infrastructures",
            short_name="CPSS-PFMI",
            is_quaterly=False,
            is_yearly=True,
            created_at=None,
        )

        published_date = None

        for content in cpss_pfmi_link.contents:
            if type(content) is bs4.element.NavigableString:
                year_regex = re.search(r'\d{4}|$', content)
                if year_regex is not None:
                    year = year_regex.group()
                    if year != "":
                        published_date = datetime(int(year), 1, 1)

        if published_date is None:
            continue

        year = str(published_date.year)

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

    for cpmi_pfmi_link in cpmi_pfmi_links:
        if cpmi_pfmi_link['href'].startswith("http"):
            document_url = cpmi_pfmi_link['href']
        else:
            document_url = scrapped_company.home_url + cpmi_pfmi_link['href']
        _, extension = os.path.splitext(document_url)

        scrapped_document_type = DocumentType(
            company_hash_id=scrapped_company.hash_id,
            full_name="Principles for financial market infrastructures",
            short_name="CPMI-PFMI",
            is_quaterly=False,
            is_yearly=True,
            created_at=None,
        )

        published_date = None

        for content in cpmi_pfmi_link.contents:
            if type(content) is bs4.element.NavigableString:
                year_regex = re.search(r'\d{4}|$', content)
                if year_regex is not None:
                    year = year_regex.group()
                    if year != "":
                        published_date = datetime(int(year), 1, 1)

        if published_date is None:
            continue

        year = str(published_date.year)

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

        published_date = None

        for content in iosco_link.contents:
            try:
                if type(content) is bs4.element.NavigableString:
                    quater_and_year = content[-9:-2]
                    Q_quater, year = quater_and_year.split("/")
                    quater = Q_quater.strip("Q")
                    published_date = datetime(int(year), ((int(quater) - 1) * 3) + 1, 1)
            except:
                continue
        
        if published_date is None:
            continue

        scrapped_document = Document(
            document_type_id=scrapped_document_type.hash_id,
            date_published=published_date,
            quater=quater,
            year=year,
            remote_url=document_url,
            extension=extension,
            created_at=None,
        )

        scrapped_document_types[scrapped_document_type.hash_id] = scrapped_document_type
        scrapped_documents[scrapped_document.hash_id] = scrapped_document
    
    return scrapped_company, scrapped_document_types, scrapped_documents