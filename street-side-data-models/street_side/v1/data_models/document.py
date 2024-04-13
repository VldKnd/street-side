import functools
import os
from typing import Optional
from venv import logger

from street_side.v1.data_models.base import BaseModelWithHashId


class RemoteDocument(BaseModelWithHashId):
    company_name: str
    document_type: str
    year: Optional[str] = None
    quater: Optional[str] = None
    url: str

    @functools.cached_property
    def root_relative_path(self):
        return (
            f"{self.company_name}/" +\
            f"{self.document_type}/" +\
            (f"{self.year}/" if self.year is not None else "") +\
            (f"{self.quater}/" if self.quater is not None else "")
        )
    
    @functools.cached_property
    def file_name(self):
        _, file_extension = os.path.splitext(self.url)
        return f"{self.hash_id}{file_extension}"
    
    def is_downloaded(self, path_to_root: str):
        local_path = (
            f"{path_to_root}"
            f"{self.root_relative_path}"
        )
        return os.path.exists(local_path)