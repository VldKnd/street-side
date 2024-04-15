import os
from typing import Dict

from pydantic import BaseModel

from street_side.v1.data_models.web import WebPage


class StreetSideConfiguration(BaseModel):
    scrapper_web_pages: Dict[str, WebPage]
    datastore_path: str

    @staticmethod
    def from_env_json_file() -> "StreetSideConfiguration":
        path_to_configuration_as_json = os.getenv("STREET_SIDE_CONFIGURATION_PATH")

        if path_to_configuration_as_json is None:
            raise RuntimeError(
                "Enviroment variable STREET_SIDE_CONFIGURATION_PATH is not set."
                "Can not create configuration."
            )
        
        with open(path_to_configuration_as_json, 'r') as configuration_file:
            configuration_file_as_json = configuration_file.read()

        return StreetSideConfiguration.model_validate_json(configuration_file_as_json)
