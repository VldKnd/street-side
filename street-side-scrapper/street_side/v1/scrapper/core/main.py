import argparse
from logging import getLogger

from street_side.v1.data_models.configuration import StreetSideConfiguration
from street_side.v1.storage.disk_storage import DiskStorage
from web import scrape_and_download_data

logger = getLogger(__name__)

def run():
    logger.info("Running the scrapper.")
    application_configuration = StreetSideConfiguration.from_env_json_file()
    disk_storage = DiskStorage(absolute_path_to_root=application_configuration.datastore_path)

    for web_page in application_configuration.scrapper_web_pages.values():
        scrape_and_download_data(
            webpage=web_page,
            storage=disk_storage,
        )

if __name__ == '__main__':
    run()