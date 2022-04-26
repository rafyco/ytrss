from ytrss.configuration.configuration import Configuration
from ytrss.core.factory.database import create_database
from ytrss.core.logging import logger
from ytrss.finder.url_finder import URLFinder


def prepare_urls(settings: Configuration) -> None:
    logger.info("Search for new movies:")
    finder = URLFinder(settings.conf.sources)
    queue = create_database(settings)
    for movie_task in finder.movies:
        if queue.queue_mp3(movie_task.movie, movie_task.destination):
            logger.info("Found new movie: [%s] %s [%s] => %s",
                        movie_task.movie.url,
                        movie_task.movie.title,
                        movie_task.movie.identity,
                        movie_task.destination)
        else:
            logger.debug("Element exists: %s", movie_task.movie.url)
