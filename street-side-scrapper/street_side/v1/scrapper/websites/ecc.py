import os
from datetime import datetime
from logging import getLogger
from typing import List, Set, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage

logger = getLogger(__name__)

ROMAN_TO_NATURAL = {
    "i":"1",
    "ii":"2",
    "iii":"3",
    "iv":"4",
}

def find_and_filter_links(web_page: WebPage) -> Tuple[Company, List[DocumentType], List[Document]]:
    url = web_page.url

    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    scrapped_company = Company(
        short_name="ECC",
        full_name="European Commodity Clearing",
        home_url="https://www.ecc.de/en/"
    )
    scrapped_document_types: Set[DocumentType] = set()
    scrapped_documents: List[Document] = []

    for table_row in soup.find_all('tr'):
        try:
            data_entry = {
                table_data["data-field"]:table_data.text
                for table_data in table_row.find_all('td')
            }
        except KeyError:
            logger.info(f"Failed to parse. Skipping the row {table_row}")
            continue

        if "title" not in data_entry:
            continue

        lowercase_title = data_entry['title'].lower()

        if (
            "pfmi" in lowercase_title
        ):
            a_element = table_row.find("a")
            document_url = urljoin(url, a_element['href'])
            document_type = DocumentType(
                company_hash_id=scrapped_company.hash_id,
                full_name="Principles for financial market infrastructures",
                short_name="PFMI",
                is_quaterly=False,
                is_yearly=True
            )
            scrapped_document_types.add(document_type)
            _, extension = os.path.splitext(document_url)

            date = datetime.strptime(
                data_entry['publishing_date'],
                "%Y-%m-%d"
            )
            scrapped_documents.append(
                Document(
                    document_type_id=document_type.hash_id,
                    date_published=date,
                    quater=None,
                    year=date.strftime("%Y"),
                    remote_url=document_url,
                    extension=extension,
                )
            )
        elif (
            "iosco" in lowercase_title
        ):
            a_element = table_row.find("a")
            document_url = urljoin(url, a_element['href'])
            document_type = DocumentType(
                company_hash_id=scrapped_company.hash_id,
                full_name="International Organization of Securities Commissions",
                short_name="IOSCO",
                is_quaterly=True,
                is_yearly=True
            )
            scrapped_document_types.add(document_type)
            _, extension = os.path.splitext(document_url)

            date = datetime.strptime(
                data_entry['publishing_date'],
                "%Y-%m-%d"
            )

            quater_as_roman_number_and_year = lowercase_title.split(" ")[-1]
            quater_as_roman_number, year = quater_as_roman_number_and_year.split("/")
            quater = ROMAN_TO_NATURAL[quater_as_roman_number]

            scrapped_documents.append(
                Document(
                    document_type_id=document_type.hash_id,
                    date_published=date,
                    quater=quater,
                    year=year,
                    remote_url=document_url,
                    extension=extension,
                )
            )
        else:
            continue
    
    return scrapped_company, list(scrapped_document_types), scrapped_documents