import asyncio
import os
import sys
from locks import Mutex

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.destination import Destination
from ytrss.core.entity.downloader import DownloaderError
from ytrss.core.entity.movie import Movie
from ytrss.core.factory.database import create_database
from ytrss.core.factory.downloader import create_downloader
from ytrss.core.helpers.logging import logger
from ytrss.database.database import Database, DatabaseStatus


async def download_movie(configuration: Configuration, movie: Movie, destination: Destination) -> None:
    """ Download movie

    This function download movie and save in destination, but it not check any conditions.
    """
    downloader = create_downloader(configuration)
    downloaded_movie = downloader.download(movie)
    os.makedirs('/tmp/ytrss', exist_ok=True)
    with Mutex(f'/tmp/ytrss/destination.{destination.identity}.lock', timeout=5.0):
        destination.save(downloaded_movie.data_paths)


async def download_task(
        configuration: Configuration,
        movie: Movie,
        destination_id: DestinationId,
        database: Database
) -> bool:
    """ Download movie

    The function make a lock on movie, download it and send to destination. It also checks if file
    can be downloaded and return with False value if not.
    """
    os.makedirs('/tmp/ytrss', exist_ok=True)
    try:
        with Mutex(f'/tmp/ytrss/movie-{movie.identity}.lock'):
            if not database.is_new(movie, destination_id):
                return False
            if not movie.is_ready:
                logger.warning("Movie is not ready to download [%s] %s",
                               movie.url,
                               movie.title)
                database.change_type(movie, DatabaseStatus.WAIT)
                return False
            destination = configuration.conf.destination_manager[destination_id]
            try:
                database.change_type(movie, DatabaseStatus.PROGRESS)
                await download_movie(configuration, movie, destination)
                logger.info("Movie downloaded: [%s] %s",
                            movie.url,
                            movie.title)
                database.change_type(movie, DatabaseStatus.DONE)
                return True
            except DownloaderError:
                logger.error("Cannot download movie: [%s] %s",
                             movie.url,
                             movie.title)
                database.change_type(movie, DatabaseStatus.ERROR)
    except BlockingIOError:
        logger.error("Cannot download movie: [%s] %s",
                     movie.url,
                     movie.title)
    return False


def download_all_movies(configuration: Configuration) -> int:
    """ Download all movies.

    This function download all files from database and send it to destination place. All the
    movies are download as a separate async task.
    """

    logger.info("Starting download movies:")
    try:
        database = create_database(configuration)
        loop = asyncio.get_event_loop()
        outputs = loop.run_until_complete(asyncio.gather(
            *[download_task(configuration, movie, destination, database) for movie, destination in database.movies()]
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
