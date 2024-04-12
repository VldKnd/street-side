from typing import List

from pydantic import BaseModel
from street_side_data_models.v1.web import WebPage


class ScrapperConfiguration(BaseModel):
    web_pages: List[WebPage]