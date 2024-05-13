import os
import re
from datetime import datetime
from logging import getLogger
from typing import Any, Dict, Tuple

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
                content.strip("\n").strip(" ").strip("'\n").startswith('CPMI-IOSCO')
                and
                "PFMI" not in content.strip("\n").strip(" ").strip("'\n")
            ):
                return True
        except:
            continue
    return False

def pfmi_filter(link) -> bool:
    for content in link.contents:
        try:
            if ("PFMI" in content.strip("\n").strip(" ").strip("'\n")):
                return True
        except:
            continue
    return False

def find_and_filter_links(web_page: WebPage) -> Tuple[
        Company,
        Dict[str, DocumentType],
        Dict[str, Document]
    ]:
    home_url = "https://clear.cboe.com"
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
    pfmi_links = filter(pfmi_filter, links)

    scrapped_company = Company(
        short_name="Cboe",
        full_name="Chicago Board Options Exchange",
        home_url=home_url,
        created_at=None,
        updated_at=None
    )

    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

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

        published_date = None

        for content in pfmi_link.contents:
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
            if type(content) is bs4.element.NavigableString:
                cleaned_content = content.strip("\n"
                    ).strip(" ").strip("\n").strip(
                        "CPMI-IOSCO Quantitative Disclosure - "
                    ).strip("– ")
                
                if cleaned_content != "":
                    published_date = datetime.strptime(cleaned_content, "%d %B %Y")

        if published_date is None:
            continue
        
        quater = str((published_date.month-1)//3 + 1)
        year = str(published_date.year)
            
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