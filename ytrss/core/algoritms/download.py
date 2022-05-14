import asyncio
import os
import sys
from locks import Mutex

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.destination import Destination
from ytrss.core.entity.movie import Movie
from ytrss.core.helpers.exceptions import DownloadMovieError
from ytrss.core.helpers.logging import logger
from ytrss.core.managers.manager_service import ManagerService, default_manager_service
from ytrss.database.database import DatabaseStatus


async def download_movie(
        movie: Movie,
        destination: Destination,
        manager_service: ManagerService = default_manager_service()
) -> None:
    """ Download movie

    This function download movie and save in destination, but it not check any conditions.
    """
    downloaded_movie = manager_service.plugin_manager.download_movie(movie, manager_service.configuration)
    manager_service.plugin_manager.modify_res_files(downloaded_movie, manager_service.configuration)
    os.makedirs('/tmp/ytrss', exist_ok=True)
    with Mutex(f'/tmp/ytrss/destination.{destination.identity}.lock', timeout=5.0):
        destination.save(downloaded_movie.data_paths, manager_service.templates_manager)


async def download_task(
        movie: Movie,
        destination_id: DestinationId,
        manager_service: ManagerService = default_manager_service()
) -> bool:
    """ Download movie

    The function make a lock on movie, download it and send to destination. It also checks if file
    can be downloaded and return with False value if not.
    """
    os.makedirs('/tmp/ytrss', exist_ok=True)
    try:
        with Mutex(f'/tmp/ytrss/movie-{movie.identity}.lock'):
            if not manager_service.database.is_new(movie, destination_id):
                return False
            if not movie.is_ready:
                logger.warning("Movie is not ready to download [%s] %s",
                               movie.url,
                               movie.title)
                manager_service.database.change_type(movie, DatabaseStatus.WAIT)
                return False
            destination = manager_service.destination_manager[destination_id]
            try:
                manager_service.database.change_type(movie, DatabaseStatus.PROGRESS)
                await download_movie(movie, destination)
                logger.info("Movie downloaded: [%s] %s",
                            movie.url,
                            movie.title)
                manager_service.database.change_type(movie, DatabaseStatus.DONE)
                return True
            except DownloadMovieError:
                logger.error("Cannot download movie: [%s] %s",
                             movie.url,
                             movie.title)
                manager_service.database.change_type(movie, DatabaseStatus.ERROR)
    except BlockingIOError:
        logger.error("Cannot download movie: [%s] %s",
                     movie.url,
                     movie.title)
    return False


def download_all_movies(manager_service: ManagerService = default_manager_service()) -> int:
    """ Download all movies.

    This function download all files from database and send it to destination place. All the
    movies are download as a separate async task.
    """

    logger.info("Starting download movies:")
    try:
        loop = asyncio.get_event_loop()
        outputs = loop.run_until_complete(asyncio.gather(
            *[download_task(movie, destination) for movie, destination in
              manager_service.database.movies()]
        ))
        queue_len = len(outputs)
        downloaded = len(list(filter(lambda x: x, outputs)))
        loop.close()

    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt by user.")
        sys.exit(1)
    except Exception as ex:
        logger.error("Unexpected Error: %s", type(ex))
        raise ex
    if queue_len == 0:
        logger.warning("Cannot find url to download")
    elif queue_len >= 0 and downloaded < queue_len:
        logger.warning("Cannot download all movies %s/%s", downloaded, queue_len)
    else:
        logger.info("Download all %s movie", downloaded)
    return downloaded
