import os
import zipfile
from logging import getLogger
from typing import List, Set
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from street_side_data_models.v1.web import WebPage

logger = getLogger(__name__)

def scrape_and_download_data(webpage: WebPage):
    links = list_links(WebPage.url)
    filtered_links = filter_out_file_urls(links)

    path_to_folder = f"{workdir}/{webpage.company_name}"

    for link in filtered_links:
        try:
            if link.endswith('.zip'):
                download_unzip_file(link, path_to_folder)
            else:
                download_file(link, path_to_folder)
        except Exception as e:
            logger.error(f"Error downloading {link}. {e}")

def list_links(url: str) -> List[str]:
    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')

    results = [
        urljoin(url, a['href']) for a in soup.find_all('a', href=True)
    ]

    return results

def filter_out_file_urls(urls: List[str]) -> List[str]:

    filtered_urls: Set[str] = set()

    for url in urls:
        url_lower = url.lower()
        cpmi_lower = 'cpmi'
        cpi_lower = 'cpi'
        quantitative_lower = 'quantitative'
        pqd_lower = 'pqd'
        disclosure_lower = 'disclosure'
        data_lower = 'data'

        if '2023' in url_lower or '2024' in url_lower:
            if cpmi_lower in url_lower:
                filtered_urls.add(url)
            if cpi_lower in url_lower:
                filtered_urls.add(url)
            if quantitative_lower in url_lower:
                filtered_urls.add(url)
            if pqd_lower in url_lower:
                filtered_urls.add(url)
            if disclosure_lower in url_lower:
                filtered_urls.add(url)
            if data_lower in url_lower:
                filtered_urls.add(url)

    return list(filtered_urls)

def download_file(url: str, path_to_folder: str) -> str:
    response = requests.get(url)
    file_name = url.split('/')[-1]
    file_path = f"{path_to_folder}/{file_name}"
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path


def download_unzip_file(url: str, path_to_folder: str):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    file_path = f"{path_to_folder}/{file_name}"

    with open(file_path, 'wb') as file:
        file.write(response.content)

    if file_name.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(path_to_folder)

        os.remove(file_path)

