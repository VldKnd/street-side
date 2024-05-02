
from typing import Callable, Dict, List, NewType, Tuple

import requests
from bs4 import BeautifulSoup
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.web import WebPage

ScrapperFunctionType = NewType(
    'ScrapperFunctionType',
    Dict[str, Callable[[WebPage], Tuple[Company, List[DocumentType], List[Document]]]]
)
