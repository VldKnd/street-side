import argparse
import json
from logging import getLogger

from configuration import ScrapperConfiguration
from street_side.v1.storage.disk_storage import DiskStorage
from web import scrape_and_download_data

logger = getLogger(__name__)

def get_arguments():
    parser = argparse.ArgumentParser(description='Simple scrapper for financial clearing documents.')
    
    parser.add_argument(
        '-d', '--datastore',
        help='Absolute path to folder, where data will be stored.',
        required=True,
        dest="path_to_datastore"
    )

    parser.add_argument(
        '-c','--configuration',
        help='Absolute path to configuration of scrapper.',
        required=True,
        dest="path_to_configuration"
    )

    args = vars(parser.parse_args())
    return args

def run(path_to_datastore: str, path_to_configuration: str):
    logger.info("Running the scrapper.")
    disk_storage = DiskStorage(STREET_SIDE_DATASTORE_PATH=path_to_datastore)

    configuration_file = open(path_to_configuration, 'r')
    configuration = json.load(configuration_file)
    configuration_file.close()
    
    scrapper_configuration = ScrapperConfiguration.model_validate(configuration)
    number_of_web_pages = len(scrapper_configuration.web_pages)

    logger.info(f"Configuration has {number_of_web_pages} links.")

    for i, web_page in enumerate(scrapper_configuration.web_pages):
        logger.info(f"{i + 1}/{number_of_web_pages} \t Scrapping {web_page.company_name}")
        scrape_and_download_data(
            webpage=web_page,
            storage=disk_storage,
        )

if __name__ == '__main__':
    keyword_arguments = get_arguments()
    run(**keyword_arguments)