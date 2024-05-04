
import os
import re
import time
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

def iosco_filter(table_row) -> bool:
    row_text = table_row.get_text()
    return "ICE Clear Europe" in row_text and\
            "DOWNLOAD" in row_text and\
            "CDS" not in row_text and\
            "Futures and Options" not in row_text

def find_and_filter_links(web_page: WebPage) -> Tuple[
        Company,
        Dict[str, DocumentType],
        Dict[str, Document]
    ]:
    home_url = "https://www.ice.com"
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
    
    try:
        driver.find_element(
            by=By.XPATH,
            value='//*[@id="integration-id-dd193e6"]/div/div[1]/div/button[2]'
        ).click()
        time.sleep(1)
    except:
        pass
    content = driver.page_source
    soups = [BeautifulSoup(content, 'html.parser')]

    try:
        while True:
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="integration-id-dd193e6"]/div/div[2]/div[2]/div[2]/div[2]/ul/li[7]/a'
            ).click()

            time.sleep(1)
            content = driver.page_source
            soups.append(BeautifulSoup(content, 'html.parser'))
    except:
        driver.quit()

    scrapped_company = Company(
        short_name="ICE Europe",
        full_name="Intercontinental Exchange Credit (ICE Europe)",
        home_url=home_url,
        created_at=None
    )
    scrapped_document_types: Dict[str, DocumentType] = {}
    scrapped_documents: Dict[str, Document] = {}

    for soup in soups:
        table_rows = soup.find_all("tr")
        iosco_table_rows = filter(iosco_filter, table_rows)

        for iosco_row in iosco_table_rows:
            archive_link = iosco_row.find('a')
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

            year_regex = re.search(r'\d{4}|$', archive_link['href'])
            quater_regex = re.search(r'Q\d|$', archive_link['href'])

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
                quater=quater,
                year=year,
                remote_url=document_url,
                extension=extension,
                created_at=None,
            )

            scrapped_document_types[scrapped_document_type.hash_id] = scrapped_document_type
            scrapped_documents[scrapped_document.hash_id] = scrapped_document
    return scrapped_company, scrapped_document_types, scrapped_documents