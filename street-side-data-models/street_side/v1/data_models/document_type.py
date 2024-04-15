from street_side.v1.data_models.base import BaseModelWithHashId


class DocumentType(BaseModelWithHashId):
    company_hash_id: str
    full_name: str
    short_name: str
    is_quaterly: bool
    is_yearly: bool
