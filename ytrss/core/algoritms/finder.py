from ytrss.configuration.configuration import Configuration
from ytrss.core.factory.database import create_database
from ytrss.core.helpers.logging import logger


def prepare_urls(configuration: Configuration) -> None:
    logger.info("Search for new movies:")
    queue = create_database(configuration)
    for movie, destination in configuration.conf.sources_manager.movies:
        if queue.queue_mp3(movie, destination):
            logger.info("Found new movie: [%s] %s [%s] => %s",
                        movie.url,
                        movie.title,
                        movie.identity,
                        destination)
        else:
            logger.debug("Element exists: %s", movie.url)
