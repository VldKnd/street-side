import os
from typing import Dict

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from street_side.v1.data_models.web import WebPage


class SharedSettings(BaseSettings):
    STREET_SIDE_DATASTORE_PATH: str = Field(default=...)
    POSTGRES_DSN: str = Field(default=...)


class ScrapperConfiguration(BaseModel):
    scrapper_web_pages: Dict[str, WebPage]
    
    @staticmethod
    def from_env_json_file() -> "ScrapperConfiguration":
        path_to_configuration_as_json = os.getenv("SCRAPPER_CONFIGURATION_PATH")

        if path_to_configuration_as_json is None:
            raise RuntimeError(
                "Enviroment variable SCRAPPER_CONFIGURATION_PATH is not set."
                "Can not create configuration."
            )
        
        with open(path_to_configuration_as_json, 'r') as configuration_file:
            configuration_file_as_json = configuration_file.read()

        return ScrapperConfiguration.model_validate_json(configuration_file_as_json)
