from logging import getLogger
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from street_side.v1.data_models.document import RemoteDocument
from street_side.v1.data_models.web import WebPage

logger = getLogger(__name__)

ROMAN_TO_NATURAL = {
    "i":"1",
    "ii":"2",
    "iii":"3",
    "iv":"4",
}

def find_and_filter_links(web_page: WebPage) -> List[RemoteDocument]:
    url = web_page.url

    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    scrapped_documents: List[RemoteDocument] = []

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
            scrapped_documents.append(
                RemoteDocument(
                    company_name="ECC",
                    document_name="PFMI",
                    url=document_url,
                )
            )

        elif (
            "iosco" in lowercase_title
        ):
            a_element = table_row.find("a")
            document_url = urljoin(url, a_element['href'])
            quater_as_roman_number_and_year = lowercase_title.split(" ")[-1]
            quater_as_roman_number, year = quater_as_roman_number_and_year.split("/")
            quater = ROMAN_TO_NATURAL[quater_as_roman_number]

            scrapped_documents.append(
                RemoteDocument(
                    company_name="ECC",
                    document_name="IOSCO",
                    year=year,
                    quater=quater,
                    url=document_url,
                )
            )
        else:
            continue
    
    return scrapped_documents