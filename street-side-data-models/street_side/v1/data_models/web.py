from pydantic import BaseModel


class WebPage(BaseModel):
    company_name: str
    url: str