import json
from logging import getLogger

from configuration import ScrapperConfiguration
from web import scrape_and_download_data

logger = getLogger(__name__)

DATASTORE_PATH = "datastore"
PATH_TO_CONFIGURATION = "street_side_scrapper/v1/websites/ecc_only.json"

def run():
    logger.info("Running the scrapper.")

    configuration_file = open(PATH_TO_CONFIGURATION, 'r')
    configuration = json.load(configuration_file)
    configuration_file.close()
    
    scrapper_configuration = ScrapperConfiguration.model_validate(configuration)
    number_of_web_pages = len(scrapper_configuration.web_pages)

    logger.info(f"Configuration has {number_of_web_pages} links.")

    for i, web_page in enumerate(scrapper_configuration.web_pages):
        logger.info(f"{i + 1}/{number_of_web_pages} \t Scrapping {web_page.company_name}")
        scrape_and_download_data(
            webpage=web_page,
            workdir=DATASTORE_PATH,
        )

if __name__ == '__main__':
    run()