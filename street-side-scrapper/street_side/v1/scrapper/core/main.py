import asyncio
from logging import getLogger

from street_side.v1.data_models.configuration import StreetSideConfiguration
from street_side.v1.storage.document_storage import DocumentStorage
from web import scrape_and_download_data

logger = getLogger(__name__)

def run():
    logger.info("Running the scrapper.")
    application_configuration = StreetSideConfiguration.from_env_json_file()
    document_storage = DocumentStorage(
        path_to_document_storage=application_configuration.datastore_path,
        postgres_dsn=application_configuration.postgres_dsn,
    )

    for web_page in application_configuration.scrapper_web_pages.values():
        scrape_and_download_data(
            webpage=web_page,
            storage=document_storage,
        )
                                 
if __name__ == '__main__':
    run()