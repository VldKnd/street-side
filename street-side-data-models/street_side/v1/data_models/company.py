
import datetime

from street_side.v1.data_models.base import FrozenBaseModelWithHashId


class Company(FrozenBaseModelWithHashId):
    short_name: str
    full_name: str
    home_url: str
    created_at: datetime.datetime | None = None
