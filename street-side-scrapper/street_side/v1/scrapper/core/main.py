from logging import getLogger

from street_side.v1.data_models.configuration import ScrapperConfiguration, SharedSettings
from street_side.v1.storage.document_storage import DocumentStorage
from web import scrape_and_download_data

APPLICATION_SETTINGS = SharedSettings()

logger = getLogger(__name__)

def run():
    logger.info("Running the scrapper.")
    application_configuration = ScrapperConfiguration.from_env_json_file()
    document_storage = DocumentStorage(
        path_to_document_storage=APPLICATION_SETTINGS.STREET_SIDE_DATASTORE_PATH,
        postgres_dsn=APPLICATION_SETTINGS.POSTGRES_DSN,
    )

    for web_page in application_configuration.scrapper_web_pages.values():
        scrape_and_download_data(
            webpage=web_page,
            storage=document_storage,
        )
                                 
if __name__ == '__main__':
    run()