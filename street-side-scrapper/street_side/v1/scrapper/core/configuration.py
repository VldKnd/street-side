from typing import List

from pydantic import BaseModel
from street_side.v1.data_models.web import WebPage

class ScrapperConfiguration(BaseModel):
    web_pages: List[WebPage]