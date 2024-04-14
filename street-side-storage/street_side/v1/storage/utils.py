import os
from logging import getLogger
from typing import Union

import requests
from street_side.v1.data_models.document import RemoteDocument

logger = getLogger(__name__)

def download_file(url: str, file_path: str) -> bool:
    try:
        os.makedirs(name=os.path.dirname(file_path), exist_ok=True)
        response = requests.get(url)
        save_file(response.content, file_path)
        return True
    except Exception as e:
        logger.error(f"Failed to download file from {url}. {e}")
        return False

def save_file(content: Union[bytes, str], file_path: str) -> bool:
    try:
        os.makedirs(name=os.path.dirname(file_path), exist_ok=True)
        mode = (
            ("wb+" if type(content) is bytes else "") +\
            ("w+" if type(content) is str else "")
        )
        
        with open(file_path, mode) as file:
            file.write(content)
        return True
    except Exception as e:
        logger.error(f"Failed to save file in {file_path}. {e}")
        return False
    

def get_document_root_relative_path(document: RemoteDocument):
    return (
        f"{document.company_name}/" +\
        f"{document.document_type}/" +\
        (f"{document.year}/" if document.year is not None else "") +\
        (f"{document.quater}/" if document.quater is not None else "") +\
        (f"{document.hash_id}")
    )

def get_document_file_name(document: RemoteDocument):
    _, file_extension = os.path.splitext(document.url)
    return f"file{file_extension}"

def get_document_metadata_name(document: RemoteDocument):
    return f"metadada.json"
