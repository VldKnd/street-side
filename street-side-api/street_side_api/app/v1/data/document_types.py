import datetime

import pydantic


class DocumentTypeGetRequestResponse(pydantic.BaseModel):
    company_hash_id: str
    full_name: str
    short_name: str
    is_quaterly: bool
    is_yearly: bool
    created_at: datetime.datetime | None
    hash_id: str
