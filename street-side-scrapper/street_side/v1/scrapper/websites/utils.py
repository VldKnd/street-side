import os
from logging import getLogger

import requests

logger = getLogger(__name__)

def download_file(url: str, path_to_folder: str, file_name: str) -> str:
    os.makedirs(name=path_to_folder, exist_ok=True)
    response = requests.get(url)
    file_path = f"{path_to_folder}/{file_name}"

    with open(file_path, 'wb+') as file:
        file.write(response.content)

    return file_path