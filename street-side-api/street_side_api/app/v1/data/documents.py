import datetime
from typing import Optional

import pydantic


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