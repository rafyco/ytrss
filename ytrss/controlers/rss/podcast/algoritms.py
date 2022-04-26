from ytrss.configuration.configuration import Configuration
from ytrss.core.logging import logger


def rss_generate(configuration: Configuration) -> None:
    for destination in configuration.conf.destination_manager.destinations:
        logger.info("Generate output: %s", destination.identity)
        destination.on_finish()
