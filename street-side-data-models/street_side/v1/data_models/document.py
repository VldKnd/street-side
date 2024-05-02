import datetime
import os
from typing import Optional

import pydantic

from street_side.v1.data_models.base import FrozenBaseModelWithHashId


class Document(FrozenBaseModelWithHashId):
    document_type_id: str
    date_published: datetime.datetime | None = pydantic.Field(None,  exclude=True)
    quater: Optional[str] = None
    year: Optional[str] = None
    remote_url: str
    extension: str
    created_at: datetime.datetime | None = pydantic.Field(None,  exclude=True)

    def get_file_name_with_extension(self):
        remote_file_name_with_extension = os.path.basename(self.remote_url)
        remote_file_name, extension = os.path.splitext(remote_file_name_with_extension)
        return f"{remote_file_name}_{self.hash_id}{extension}"