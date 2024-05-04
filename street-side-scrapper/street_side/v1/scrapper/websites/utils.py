
from typing import Callable, Dict, List, NewType, Tuple

from selenium.webdriver.chrome.options import Options
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage

ScrapperFunctionType = NewType(
    'ScrapperFunctionType',
    Dict[str, Callable[[WebPage], Tuple[Company, List[DocumentType], List[Document]]]]
)

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options