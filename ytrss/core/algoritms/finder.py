from ytrss.core.helpers.logging import logger
from ytrss.core.managers.manager_service import ManagerService, default_manager_service


def prepare_urls(manager_service: ManagerService = default_manager_service()) -> bool:
    """ Find urls and save to database

    The algorithm search for movies in source and save to database when some new movies are searched.
    """
    logger.info("Search for new movies:")
    queue = manager_service.database
    for movie, destination in manager_service.sources_manager.movies:
        if queue.queue_mp3(movie, destination):
            logger.info("Found new movie: [%s] %s [%s] => %s",
                        movie.url,
                        movie.title,
                        movie.identity,
                        destination)
        else:
            logger.debug("Element exists: %s", movie.url)
    return True
