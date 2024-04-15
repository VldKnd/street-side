from pydantic import BaseModel


class WebPage(BaseModel):
    company_name: str
    full_name: str
    url: str