import asyncio
import base64
import logging
import os
import time
from typing import Dict, List, Tuple

import asyncpg
import pydantic
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from street_side.v1.data_models.company import Company
from street_side.v1.data_models.document import Document
from street_side.v1.data_models.document_type import DocumentType
from street_side.v1.data_models.excel import ExcelFile

from street_side.v1.repositories.company import CompanyRepository
from street_side.v1.repositories.document import DocumentRepository
from street_side.v1.repositories.document_type import DocumentTypeRepository

LOGGER = logging.getLogger(__name__)

class DocumentStorage(pydantic.BaseModel):
    path_to_document_storage: str
    postgres_dsn: str

    async def get_excel_file_by_document_hash_id(self, document_hash_id: str) -> ExcelFile:
        document = await self.get_document_by_hash_id(document_hash_id=document_hash_id)
        path_to_file = self.get_path_to_file_from_document(document)
        
        if not os.path.exists(path_to_file):
            raise RuntimeError(
                f"Document {path_to_file} is not present on disk and can not be loaded.",
                "It is likely not present on the disk."
            )
        
        return ExcelFile.get_excel_file_from_local_disk(path_to_file=path_to_file)

    async def get_file_path_and_name_by_document_hash_id(self, document_hash_id: str) -> Tuple[str, str]:
        connection = await asyncpg.connect(self.postgres_dsn)

        document = await self.get_document_by_hash_id(
            document_hash_id=document_hash_id,
            connection=connection
        )
        document_type = await self.get_document_type_by_hash_id(
            document_type_hash_id=document.document_type_id,
            connection=connection
        )
        company = await self.get_company_by_hash_id(
            company_hash_id=document_type.company_hash_id,
            connection=connection
        )

        await connection.close()
    
        file_path = f"{self.path_to_document_storage}/{document.get_file_name_with_extension()}"

        document_pretty_name = f"{document.year}" + (document.quater is not None)*f"_Q{document.quater}"
        file_name = (
            f"{company.short_name}_"
            f"{document_type.short_name}_"
            f"{document_pretty_name}"
            f"{document.extension}"
        )

        return file_path, file_name

    async def get_file_as_base64_by_document_hash_id(self, document_hash_id: str) -> str:
        document = await self.get_document_by_hash_id(document_hash_id=document_hash_id)
        file_as_base64 = self.file_as_base64_from_local_disk(document=document)
        return file_as_base64

    async def get_company_by_hash_id(
            self,
            company_hash_id: str,
            connection: asyncpg.Connection |  None = None,
        ) -> Company:
        if connection is None:
            _connection = await asyncpg.connect(self.postgres_dsn)
            company_repository = CompanyRepository(connection=_connection)
            companies = await company_repository.fetch([company_hash_id])
            await _connection.close()
        else:
            company_repository = CompanyRepository(connection=connection)
            companies = await company_repository.fetch([company_hash_id])

        company = companies.get(company_hash_id, None)

        if company is None:
            raise RuntimeError(
                f"Company with id {company_hash_id} was found in database."
            )
        
        return company
    
    async def get_document_type_by_hash_id(
            self,
            document_type_hash_id: str,
            connection: asyncpg.Connection |  None = None,
        ) -> DocumentType:
        if connection is None:
            _connection = await asyncpg.connect(self.postgres_dsn)
            document_type_repository = DocumentTypeRepository(connection=_connection)
            document_types = await document_type_repository.fetch([document_type_hash_id])
            await _connection.close()
        else:
            document_type_repository = DocumentTypeRepository(connection=connection)
            document_types = await document_type_repository.fetch([document_type_hash_id])

        document_type = document_types.get(document_type_hash_id, None)

        if document_type is None:
            raise RuntimeError(
                f"Document type with id {document_type_hash_id} was found in database."
            )
        
        return document_type

    async def get_document_by_hash_id(
            self,
            document_hash_id: str,
            connection: asyncpg.Connection |  None = None,
        ) -> Document:
        if connection is None:
            _connection = await asyncpg.connect(self.postgres_dsn)
            document_repository = DocumentRepository(connection=_connection)
            documents = await document_repository.fetch([document_hash_id])
            await _connection.close()
        else:
            document_repository = DocumentRepository(connection=connection)
            documents = await document_repository.fetch([document_hash_id])

        document = documents.get(document_hash_id, None)

        if document is None:
            raise RuntimeError(
                f"Document with id {document_hash_id} was found in database."
            )
        
        return document
        
    async def get_documents_by_document_type_hash_id(self, document_type_hash_id: str) -> List[Document]:
        GET_DOCUMENTS_QUERY = """
            SELECT * FROM "v1"."documents"
            WHERE document_type_id=$1;
        """

        connection = await asyncpg.connect(self.postgres_dsn)
        response_rows = await connection.fetch(
            GET_DOCUMENTS_QUERY,
            document_type_hash_id
        )

        return [
            Document(
                document_type_id=row["document_type_id"],
                date_published=row["date_published"],
                quater=row["quater"],
                year=row["year"],
                remote_url=row["remote_url"],
                extension=row["extension"],
                created_at=row["created_at"]
            ) for row in response_rows
        ]
        
    async def get_document_types_by_company_hash_id(self, company_hash_id: str) -> List[DocumentType]:
        GET_DOCUMENT_TYPES_QUERY = """
            SELECT * FROM "v1"."document_types"
            WHERE company_hash_id=$1;
        """

        connection = await asyncpg.connect(self.postgres_dsn)
        response_rows = await connection.fetch(
            GET_DOCUMENT_TYPES_QUERY,
            company_hash_id
        )

        return [
            DocumentType(
                company_hash_id=row['company_hash_id'],
                full_name=row['full_name'],
                short_name=row['short_name'],
                is_quaterly=row['is_quaterly'],
                is_yearly=row['is_yearly'],
                created_at=row['created_at'],
            ) for row in response_rows
        ]
    
    async def get_all_companies(self) -> List[Company]:
        GET_COMPANIES_QUERY = """
            SELECT * FROM "v1"."companies";
        """
        connection = await asyncpg.connect(self.postgres_dsn)
        response_rows = await connection.fetch(GET_COMPANIES_QUERY)
        return [
            Company(
                short_name=row['short_name'],
                full_name=row['full_name'],
                home_url=row['home_url'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            ) for row in response_rows
        ]
    
    def get_path_to_file_from_document(self, document: Document) -> str:
        return f"{self.path_to_document_storage}/{document.get_file_name_with_extension()}"
    
    def file_as_base64_from_local_disk(self, document: Document) -> str:
        path_to_file = self.get_path_to_file_from_document(document)

        if not os.path.exists(path_to_file):
            raise RuntimeError(
                f"Document {path_to_file} is not present on disk and can not be loaded.",
                "It is likely not present on the disk."
            )
        
        file_on_local_disk = open(path_to_file, mode='rb')
        file_as_bytes = file_on_local_disk.read()
        file_on_local_disk.close()
        file_as_base64 = (base64.b64encode(file_as_bytes)).decode('ascii')

        return file_as_base64
    
    def download_document_to_local_disk(self, document: Document):
        path_to_file = self.get_path_to_file_from_document(document)
        if os.path.exists(path_to_file): return
        
        headers = {
            "Accept-Encoding":"gzip, deflate, br",
            "User-Agent":"Java-http-client/",
            "Accept-Language":"en-US,en;q=0.9"
        }
        
        response = requests.get(
            url=document.remote_url,
            headers=headers,
            timeout=5,
        )
        content = response.content

        file_on_local_disk = open(path_to_file, mode='wb+')
        file_on_local_disk.write(content)
        file_on_local_disk.close()

    async def postgres_insert_scrapping_result(self, companies: Dict[str, Company], document_types: Dict[str, DocumentType], documents: Dict[str, Document]):
        [
            company_connection,
            document_repository_connection,
            document_type_repository_connection
        ] = await asyncio.gather(
            asyncpg.connect(self.postgres_dsn),
            asyncpg.connect(self.postgres_dsn),
            asyncpg.connect(self.postgres_dsn)
        )

        company_repository = CompanyRepository(connection=company_connection)
        document_repository = DocumentRepository(connection=document_repository_connection)
        document_type_repository = DocumentTypeRepository(connection=document_type_repository_connection)

        await asyncio.gather(
            document_repository.insert(documents=documents),
            document_type_repository.insert(document_types=document_types),
            company_repository.insert(companies=companies),
        )

        await asyncio.gather(
            company_connection.close(),
            document_repository_connection.close(),
            document_type_repository_connection.close()
        )

    def insert_and_download_scrapping_result(self, company: Company, document_types: Dict[str, DocumentType], documents: Dict[str, Document]):
        downloaded_documents: Dict[str, Document] = {}
        for _, document in documents.items():
            try:
                self.download_document_to_local_disk(document=document)
                downloaded_documents[document.hash_id] = document
            except Exception as e:
                LOGGER.error(
                    f"Failed to download document {document}. It will not be inserted. {e}"
                )

        if len(downloaded_documents) < 1:
            return

        kept_document_types_hash_ids = {
            downloaded_document.document_type_id for
            downloaded_document in downloaded_documents.values()
        }

        asyncio.run(
            self.postgres_insert_scrapping_result(
                companies={company.hash_id:company},
                document_types={
                    document_type_hash_id:document_types[document_type_hash_id]
                    for document_type_hash_id in kept_document_types_hash_ids
                },
                documents=documents,
            )
        )
