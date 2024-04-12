from typing import Any, Dict, List, Protocol

from street_side_data_models.v1.document import ScrappedDocument


class _Storage(Protocol):
    """
    Generic repository for scrapped files.
    """

    async def fetch(self, identifiers: List[str]) -> Dict[str, Any]:
        ...

    async def insert(self, documents: List[ScrappedDocument]) -> List[str]:
        ...

