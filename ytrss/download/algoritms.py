"""
Module with algorithms that download files
"""
import asyncio
import os
import sys
from locks import Mutex

from ytrss.configuration.configuration import Configuration
from ytrss.core.entity.destination import Destination
from ytrss.core.entity.downloader import DownloaderError
from ytrss.core.entity.movie import Movie
from ytrss.core.factory.database import create_database
from ytrss.core.factory.downloader import create_downloader
from ytrss.core.logging import logger
from ytrss.database.database import Database, DatabaseStatus
from ytrss.database.entity.movie_task import MovieTask


async def download_movie(configuration: Configuration, movie: Movie, destination: Destination) -> None:
    """
    Download one movie and save it to destination.
    """
    downloader = create_downloader(configuration)
    files = downloader.download(movie)
    os.makedirs('/tmp/ytrss', exist_ok=True)
    with Mutex(f'/tmp/ytrss/destination.{destination.identity}.lock', timeout=10.0):
        destination.save(files)


async def download_task(
        configuration: Configuration,
        movie_task: MovieTask,
        database: Database
) -> bool:
    """
    Download movie from task with check if is it safe.
    """
    os.makedirs('/tmp/ytrss', exist_ok=True)
    try:
        with Mutex(f'/tmp/ytrss/movie-{movie_task.movie.identity}.lock'):
            if not database.is_new(movie_task.movie, movie_task.destination):
                return False
            if not movie_task.movie.is_ready:
                logger.warning("Movie is not ready to download [%s] %s",
                               movie_task.movie.url,
                               movie_task.movie.title)
                database.change_type(movie_task.movie, DatabaseStatus.WAIT)
                return False
            destination = configuration.conf.destination_manager[movie_task.destination]
            try:
                database.change_type(movie_task.movie, DatabaseStatus.PROGRESS)
                await download_movie(configuration, movie_task.movie, destination)
                logger.info("Movie downloaded: [%s] %s",
                            movie_task.movie.url,
                            movie_task.movie.title)
                database.change_type(movie_task.movie, DatabaseStatus.DONE)
                return True
            except DownloaderError:
                logger.error("Cannot download movie: [%s] %s",
                             movie_task.movie.url,
                             movie_task.movie.title)
                database.change_type(movie_task.movie, DatabaseStatus.ERROR)
    except BlockingIOError:
        logger.error("Cannot download movie: [%s] %s",
                     movie_task.movie.url,
                     movie_task.movie.title)
    return False


def download_all_movies(configuration: Configuration) -> int:
    """
    Download all movies saved it to destination.
    """

    logger.info("Starting download movies:")
    try:
        database = create_database(configuration)
        loop = asyncio.get_event_loop()
        outputs = loop.run_until_complete(asyncio.gather(
            *[download_task(configuration, movie_task, database) for movie_task in database.movies()]
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
    if queue_len >= 0 and downloaded < queue_len:
        logger.warning("Cannot download all movies")
    return downloaded
