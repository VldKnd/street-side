import functools
import os
from typing import Optional
from venv import logger

from street_side.v1.data_models.base import BaseModelWithHashId


class DocumentType(BaseModelWithHashId):
    name: str
    yearly: bool
    quaterly: bool

class RemoteDocument(BaseModelWithHashId):
    company_name: str
    document_name: str
    year: Optional[str] = None
    quater: Optional[str] = None
    url: str