from logging import getLogger
from typing import List

from fastapi import HTTPException, status
from fastapi.responses import FileResponse

import street_side_api.app.v1.methods.data
from street_side_api.app.v1.data.company import CompanyGetRequestResponse
from street_side_api.app.v1.data.document_types import DocumentTypeGetRequestResponse
from street_side_api.app.v1.data.documents import DocumentGetRequestResponse

logger = getLogger(__name__)

async def download_file_by_document_hash_id(document_hash_id: str) -> FileResponse:
    try:
        file_path, file_name = await street_side_api.app.v1.methods.data.get_file_path_and_name_by_document_hash_id(
            document_hash_id=document_hash_id,
        )
    except Exception as e:
        logger.exception(f"Error getting file from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return FileResponse(
            path=file_path,
            media_type='application/octet-stream',
            filename=file_name
        )

async def get_file_as_base64_by_document_hash_id(document_hash_id: str) -> str:
    try:
        response = await street_side_api.app.v1.methods.data.get_file_as_base64_by_document_hash_id(
            document_hash_id=document_hash_id,
        )
    except Exception as e:
        logger.exception(f"Error getting file from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response

async def get_documents_by_document_type_hash_id(
        document_type_hash_id: str
    ) -> List[DocumentGetRequestResponse]:
    try:
        response = await street_side_api.app.v1.methods.data.get_documents_by_document_type_hash_id(
            document_type_hash_id=document_type_hash_id,
        )
    except Exception as e:
        logger.exception(f"Error getting documents from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response
    
async def get_document_types_by_company_hash_id(company_hash_id: str) -> List[DocumentTypeGetRequestResponse]:
    try:
        response = await street_side_api.app.v1.methods.data.get_document_types_by_company_hash_id(
            company_hash_id=company_hash_id
        )
    except Exception as e:
        logger.exception(f"Error getting document types from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response

async def get_all_companies() -> List[CompanyGetRequestResponse]:
    try:
        response = await street_side_api.app.v1.methods.data.get_all_companies()
    except Exception as e:
        logger.exception(f"Error getting companies from database", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return response
