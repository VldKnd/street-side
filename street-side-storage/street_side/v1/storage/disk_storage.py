import os
from logging import getLogger
from typing import List

import pydantic
from street_side.v1.data_models.document import Document

import street_side.v1.storage.utils as v1_storage_utils

logger = getLogger(__name__)

class DiskStorage(pydantic.BaseModel):
    absolute_path_to_root: str

    def get_absolute_local_path_to_document(self, document: Document):
        relative_path_to_document_folder = v1_storage_utils.get_document_root_relative_path(
            document=document
        )
        local_absolute_path = (
            f"{self.absolute_path_to_root}/"
            f"{relative_path_to_document_folder}"
        )
        return local_absolute_path

    def clean_up_document(self, document: Document):
        local_absolute_path = self.get_absolute_local_path_to_document(
            document=document
        )
        file_name = v1_storage_utils.get_document_file_name(
            document=document
        )
        metadata_name = v1_storage_utils.get_document_metadata_name(
            document=document
        )

        try:
            os.remove(f"{local_absolute_path}/{file_name}")
        except FileNotFoundError:
            message = (
                f"While deleting {document.company_name}, {document.document_name}"
                f"file not found."
            )
            logger.info(message)

        try:
            os.remove(f"{local_absolute_path}/{metadata_name}")
        except FileNotFoundError:
            message = (
                f"While deleting {document.company_name}, {document.document_name}"
                f"metadata file not found."
            )
            logger.info(message)

        while local_absolute_path != self.absolute_path_to_root:
            os.rmdir(local_absolute_path)
            local_absolute_path = os.path.dirname(local_absolute_path)

    def put(self, document: Document) -> bool:
        if self.is_document_downloaded(document):
            return True
        
        url = document.url
        local_absolute_path = self.get_absolute_local_path_to_document(
            document=document
        )
        file_name = v1_storage_utils.get_document_file_name(
            document=document
        )
        metadata_name = v1_storage_utils.get_document_metadata_name(
            document=document
        )
        document_file_path = f"{local_absolute_path}/{file_name}"
        document_metadata_path = f"{local_absolute_path}/{metadata_name}"
            
        if not v1_storage_utils.download_file(
            url=url,
            file_path=document_file_path
        ):
            return False
        
        if not v1_storage_utils.save_file(
            content=document.model_dump_json(),
            file_path=document_metadata_path
        ):
            self.clean_up_document(document=document)
            return False
        
        return True
        
    def fetch(self, identificator: str) -> Document:
        ...

    def list_companies_names(self) -> List[str]:
        return os.listdir(self.absolute_path_to_root)

    def list_company_documents_names(self, company_name: str) -> List[str]:
        path_to_company_folder = f"{self.absolute_path_to_root}/{company_name}"
        return os.listdir(path_to_company_folder)

    def list_company_document_years(
            self,
            company_name: str,
            document_type: str
        ) -> List[str]:
        ...

    def list_company_document_entries(
            self,
            company_name: str,
            document_type: str
        ) -> List[Document]:
        ...

    def is_document_downloaded(self, document: Document) -> bool:
        relative_path_to_document_folder = v1_storage_utils.get_document_root_relative_path(
            document=document
        )
        local_absolute_path = (
            f"{self.absolute_path_to_root}"
            f"{relative_path_to_document_folder}"
        )
        return os.path.exists(local_absolute_path)