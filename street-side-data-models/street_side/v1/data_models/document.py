import datetime
from typing import Optional

from street_side.v1.data_models.base import BaseModelWithHashId


class Document(BaseModelWithHashId):
    document_type_id: str
    date_published: Optional[datetime.datetime] = None
    quater: Optional[str] = None
    year: Optional[str] = None
    local_path: Optional[str] = None
    remote_url: str
    extension: str