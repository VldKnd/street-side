import os
from typing import List

import pydantic
from pydantic_settings import BaseSettings
from street_side.v1.data_models.document import RemoteDocument

import street_side.v1.storage.utils as v1_storage_utils


class DiskStorage(BaseSettings):
    absolute_path_to_root: str = pydantic.Field(alias='STREET_SIDE_DATASTORE_PATH')

    def get_absolute_local_path_to_document(self, document: RemoteDocument):
        relative_path_to_document_folder = v1_storage_utils.get_document_root_relative_path(
            document=document
        )
        local_absolute_path = (
            f"{self.absolute_path_to_root}/"
            f"{relative_path_to_document_folder}"
        )
        return local_absolute_path

    def clean_up_document(self, document: RemoteDocument):
        local_absolute_path = self.get_absolute_local_path_to_document(
            document=document
        )
        file_name = v1_storage_utils.get_document_file_name(
            document=document
        )
        metadata_name = v1_storage_utils.get_document_metadata_name(
            document=document
        )

        os.remove(f"{local_absolute_path}/{file_name}")
        os.remove(f"{local_absolute_path}/{metadata_name}")
        os.rmdir(local_absolute_path)

    def put(self, document: RemoteDocument) -> bool:
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
        
    def fetch(self, identificator: str) -> RemoteDocument:
        ...

    def list_companies(self) -> List[str]:
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
        ) -> List[RemoteDocument]:
        ...

    def is_document_downloaded(self, document: RemoteDocument) -> bool:
        relative_path_to_document_folder = v1_storage_utils.get_document_root_relative_path(
            document=document
        )
        local_absolute_path = (
            f"{self.absolute_path_to_root}"
            f"{relative_path_to_document_folder}"
        )
        return os.path.exists(local_absolute_path)