import datetime

from street_side.v1.data_models.base import FrozenBaseModelWithHashId


class DocumentType(FrozenBaseModelWithHashId):
    company_hash_id: str
    full_name: str
    short_name: str
    is_quaterly: bool
    is_yearly: bool
    created_at: datetime.datetime | None = None
