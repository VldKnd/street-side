
from logging import getLogger
from typing import List, Tuple

from street_side.v1.data_models.configuration import StreetSideConfiguration
from street_side.v1.data_models.excel import ExcelFile
from street_side.v1.data_models.response import (
    CompanyGetRequestResponse,
    DocumentGetRequestResponse,
    DocumentTypeGetRequestResponse,
)
from street_side.v1.storage.document_storage import DocumentStorage

logger = getLogger(__name__)

APPLICATION_CONFIGURATION = StreetSideConfiguration.from_env_json_file()
DOCUMENT_STORAGE = DocumentStorage(
    path_to_document_storage=APPLICATION_CONFIGURATION.datastore_path,
    postgres_dsn=APPLICATION_CONFIGURATION.postgres_dsn
)

async def get_excel_file_by_document_hash_id(document_hash_id: str) -> ExcelFile:
    return await DOCUMENT_STORAGE.get_excel_file_by_document_hash_id(
        document_hash_id=document_hash_id
    )

async def get_file_path_and_name_by_document_hash_id(document_hash_id: str) -> Tuple[str, str]:
    return await DOCUMENT_STORAGE.get_file_path_and_name_by_document_hash_id(
        document_hash_id=document_hash_id
    )

async def get_file_as_base64_by_document_hash_id(document_hash_id: str) -> str:
    document_as_base64 = await DOCUMENT_STORAGE.get_file_as_base64_by_document_hash_id(
        document_hash_id=document_hash_id
    )

    if document_as_base64 is None:
        raise RuntimeError("Document was not properly loaded. It is likely not present on the disk.")

    return document_as_base64
    
async def get_documents_by_document_type_hash_id(
        document_type_hash_id: str
    ) -> List[DocumentGetRequestResponse]:
    """
    Get documents of document type using its short name and company hash id.

    Returns
    -------
    NameResponse
        The name of the project.
    """
    documents = await DOCUMENT_STORAGE.get_documents_by_document_type_hash_id(
        document_type_hash_id=document_type_hash_id
    )

    return [
        DocumentGetRequestResponse(
            document_type_id=document.document_type_id,
            date_published=document.date_published,
            quater=document.quater,
            year=document.year,
            pretty_date=f"{document.year}" + (document.quater is not None)*f" Q{document.quater}",
            remote_url=document.remote_url,
            extension=document.extension,
            created_at=document.created_at,
            hash_id=document.hash_id,
        ) for document in documents
    ]


async def get_document_types_by_company_hash_id(company_hash_id: str) -> List[DocumentTypeGetRequestResponse]:
    document_types =  await DOCUMENT_STORAGE.get_document_types_by_company_hash_id(
        company_hash_id=company_hash_id
    )

    return [
        DocumentTypeGetRequestResponse(
            company_hash_id=document_type.company_hash_id,
            full_name=document_type.full_name,
            short_name=document_type.short_name,
            is_quaterly=document_type.is_quaterly,
            is_yearly=document_type.is_yearly,
            created_at=document_type.created_at,
            hash_id=document_type.hash_id
        ) for document_type in document_types
    ]

async def get_all_companies() -> List[CompanyGetRequestResponse]:
    """
    Get the name of the project.

    Returns
    -------
    NameResponse
        The name of the project.
    """
    companies = await DOCUMENT_STORAGE.get_all_companies()
    return [
        CompanyGetRequestResponse(
            short_name=company.short_name,
            full_name=company.full_name,
            home_url=company.home_url,
            created_at=company.created_at,
            hash_id=company.hash_id
        ) for company in companies
    ]
