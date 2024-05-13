
import datetime

import pydantic

from street_side.v1.data_models.base import FrozenBaseModelWithHashId


class Company(FrozenBaseModelWithHashId):
    short_name: str
    full_name: str
    home_url: str
    created_at: datetime.datetime | None = pydantic.Field(None,  exclude=True)
    updated_at: datetime.datetime | None = pydantic.Field(None,  exclude=True)
