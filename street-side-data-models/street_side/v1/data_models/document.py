import functools
import os
from typing import Optional
from venv import logger

from street_side.v1.data_models.base import BaseModelWithHashId


class RemoteDocument(BaseModelWithHashId):
    company_name: str
    document_type: str
    year: Optional[str] = None
    quater: Optional[str] = None
    url: str