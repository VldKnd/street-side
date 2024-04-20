import datetime

import pydantic


class CompanyGetRequestResponse(pydantic.BaseModel):
    short_name: str
    full_name: str
    home_url: str
    created_at: datetime.datetime | None
    hash_id: str
