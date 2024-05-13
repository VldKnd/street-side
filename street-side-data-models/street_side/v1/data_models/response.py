import datetime
from typing import Optional

import pydantic


class CompanyGetRequestResponse(pydantic.BaseModel):
    short_name: str
    full_name: str
    home_url: str
    created_at: datetime.datetime | None
    hash_id: str
    updated_at: datetime.datetime | None


class DocumentTypeGetRequestResponse(pydantic.BaseModel):
    company_hash_id: str
    full_name: str
    short_name: str
    is_quaterly: bool
    is_yearly: bool
    created_at: datetime.datetime | None
    hash_id: str

class DocumentGetRequestResponse(pydantic.BaseModel):
    document_type_id: str
    date_published: Optional[datetime.datetime] = None
    quater: Optional[str] = None
    year: Optional[str] = None
    pretty_date: str
    remote_url: str
    extension: str
    created_at: datetime.datetime | None
    hash_id: str