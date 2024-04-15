
from street_side.v1.data_models.base import BaseModelWithHashId


class Company(BaseModelWithHashId):
    short_name: str
    full_name: str
    home_url: str
