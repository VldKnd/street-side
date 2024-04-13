from typing import List

import pydantic
from street_side.v1.data_models.document import RemoteDocument


class DiskStorage(pydantic.BaseModel):
    absolute_path_to_root: str

    def put(self, document: RemoteDocument) -> bool:
        try:
            url = document.url
            root_relative_document_path = document.root_relative_path
            path_to_download = (
                f"{self.absolute_path_to_root}/"
                f"{root_relative_document_path}"
            )
            
            download_file(
                url=url,
                path_to_folder=path_to_download,
                file_name=document.file_name
            )
            return True
        except Exception as e:
            logger.error(f"Error downloading {url}. {e}")
            return False
    
    def fetch(self, identificator: str) -> RemoteDocument:
        ...

    def list_companies(self) -> List[str]:
        ...

    def list_company_document_types(self, company_name: str) -> List[str]:
        ...

    def get_company_document_type_metadata(
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