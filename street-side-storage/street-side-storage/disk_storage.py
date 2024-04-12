
import asyncio
from typing import Any, Dict, List

from street_side_data_models.v1.document import ScrappedDocument
from street_side_storage.interface import _Storage


class DiskStorage(_Storage):
    def __init__(self, storage_root_path: str):
        self.storage_root_path = storage_root_path

    async def fetch(self, identifiers: List[str]) -> Dict[str, Any]:
        for identifier in identifiers:
            fetch_from_storage(identifier)

    async def insert(self, documents: List[ScrappedDocument]) -> List[str]:
        ...
