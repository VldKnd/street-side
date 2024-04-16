import asyncio
import logging
from typing import Dict, List

import pydantic
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.configuration import StreetSideConfiguration
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType

from street_side.v1.repositories.company import CompanyRepository
from street_side.v1.repositories.document import DocumentRepository
from street_side.v1.repositories.document_type import DocumentTypeRepository
from street_side.v1.repositories.pool import PGPool

STREET_SIDE_CONFIGURATION = StreetSideConfiguration.from_env_json_file()
LOGGER = logging.getLogger(__name__)

class DocumentStorage(pydantic.BaseModel):
    path_to_document_storage: str = STREET_SIDE_CONFIGURATION.datastore_path

    def download_document(self, document: Document):
        ...

    def postgres_insert_scrapping_result(self, company: Company, document_types: Dict[str, DocumentType], documents: Dict[str, Document]):
        for hash_id, document in documents.items():
            try:
                self.download_document(document=document)
            except Exception as e:
                documents.pop(hash_id, None)
                LOGGER.error(
                    f"Failed to download document {document}. It will not be inserted. {e}"
                )

        if len(documents) < 1:
            return

        connection = PGPool.get_connection()

        document_repository = DocumentRepository(connection=connection)
        inserted_document_hash_ids = asyncio.run(
            main=document_repository.insert(documents=documents)
        )

        kept_document_types_hash_ids = {
            documents[inserted_document_hash_id].document_type_id for
            inserted_document_hash_id in inserted_document_hash_ids
        }

        for document_type_hash_id in document_types.keys():
            if document_type_hash_id not in kept_document_types_hash_ids:
                document_types.pop(document_type_hash_id, None)

        document_type_repository = DocumentTypeRepository(connection=connection)
        _ = asyncio.run(
            main=document_type_repository.insert(document_types=document_types)
        )

        
        