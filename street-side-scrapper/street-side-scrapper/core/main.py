import json
from logging import getLogger

from configuration import ScrapperConfiguration
from web import scrape_and_download_data

logger = getLogger(__name__)

PATH_TO_CONFIGURATION = "../websites/test.json"

def run_scrapper():
    logger.info("Running the scrapper.")

    file = open(PATH_TO_CONFIGURATION, 'r')
    configuration = json.load(file)
    file.close()

    scrapper_configuration = ScrapperConfiguration.model_validate(configuration)
    number_of_web_pages = len(scrapper_configuration.web_pages)

    logger.info(f"Configuration has {number_of_web_pages} links.")

    for i, web_page in enumerate(scrapper_configuration.web_pages):
        logger.info(f"{i + 1}/{number_of_web_pages} \t Scrapping {web_page.company_name}")

        scrape_and_download_data(
            webpage=web_page
        )

if __name__ == '__main__':
    run_scrapper()