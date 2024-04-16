import asyncio
import logging
import os
from typing import Dict

import asyncpg
import pydantic
import requests
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.configuration import StreetSideConfiguration
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType

from street_side.v1.repositories.company import CompanyRepository
from street_side.v1.repositories.document import DocumentRepository
from street_side.v1.repositories.document_type import DocumentTypeRepository

STREET_SIDE_CONFIGURATION = StreetSideConfiguration.from_env_json_file()
LOGGER = logging.getLogger(__name__)

class DocumentStorage(pydantic.BaseModel):
    path_to_document_storage: str = STREET_SIDE_CONFIGURATION.datastore_path
    postgres_dsn: str = STREET_SIDE_CONFIGURATION.postgres_dsn

    def download_document_to_local_disk(self, document: Document):
        document_path = f"{self.path_to_document_storage}/{document.file_name_with_extension}"

        if os.path.exists(document_path):
            return
        
        response = requests.get(document.remote_url)

        with open(document_path, mode='wb+') as document_on_local_disk:
            document_on_local_disk.write(response.content)

    async def postgres_insert_scrapping_result(self, companies: Dict[str, Company], document_types: Dict[str, DocumentType], documents: Dict[str, Document]):
        async with asyncpg.create_pool(self.postgres_dsn, min_size=1, max_size=1) as pool:
            async with pool.acquire() as connection:
                document_repository = DocumentRepository(connection=connection)
                document_type_repository = DocumentTypeRepository(connection=connection)
                company_repository = CompanyRepository(connection=connection)

                await asyncio.gather(
                    document_repository.insert(documents=documents),
                    document_type_repository.insert(document_types=document_types),
                    company_repository.insert(companies=companies),
                )
        
    def insert_and_download_scrapping_result(self, company: Company, document_types: Dict[str, DocumentType], documents: Dict[str, Document]):
        for hash_id, document in documents.items():
            try:
                self.download_document_to_local_disk(document=document)
            except Exception as e:
                documents.pop(hash_id, None)
                LOGGER.error(
                    f"Failed to download document {document}. It will not be inserted. {e}"
                )

        if len(documents) < 1:
            return

        kept_document_types_hash_ids = {
            document.document_type_id for
            document in documents.values()
        }

        for document_type_hash_id in document_types.keys():
            if document_type_hash_id not in kept_document_types_hash_ids:
                document_types.pop(document_type_hash_id, None)

        asyncio.run(
            self.postgres_insert_scrapping_result(
                companies={company.hash_id:company},
                document_types=document_types,
                documents=documents,
            )
        )
        
        