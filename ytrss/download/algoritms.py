"""
Module with algorithms that download files
"""
import asyncio
import logging
import os
import sys
from locks import Mutex

from ytrss.configuration.configuration import Configuration
from ytrss.core.entity.destination import Destination
from ytrss.core.entity.downloader import DownloaderError
from ytrss.core.entity.movie import Movie
from ytrss.core.factory.database import create_database
from ytrss.core.factory.downloader import create_downloader
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
                print(f"URL {movie_task.movie.url} cannot again download")
                return False
            if not movie_task.movie.is_ready:
                print(f"[{movie_task.movie.url}] movie is not ready to download")
                database.change_type(movie_task.movie, DatabaseStatus.WAIT)
                return False
            destination = configuration.conf.destination_manager[movie_task.destination]
            try:
                database.change_type(movie_task.movie, DatabaseStatus.PROGRESS)
                await download_movie(configuration, movie_task.movie, destination)
                print(f"[{movie_task.movie.url}] finish ok")
                database.change_type(movie_task.movie, DatabaseStatus.DONE)
                return True
            except DownloaderError:
                print(f"[{movie_task.movie.url}] finish error")
                database.change_type(movie_task.movie, DatabaseStatus.ERROR)
    except BlockingIOError:
        print(f"[{movie_task.movie.url}] Cannot download ")
    return False


def download_all_movie(configuration: Configuration) -> int:
    """
    Download all movie saved it to destination.
    """

    logging.info("download movie from urls")
    downloaded = 0
    try:
        database = create_database(configuration)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            *[download_task(configuration, movie_task, database) for movie_task in database.movies()]
        ))
        loop.close()

    except KeyboardInterrupt:
        print("Keyboard Interrupt by user.")
        sys.exit(1)
    except Exception as ex:
        print(f"Unexpected Error: {type(ex)}")
        raise ex
    if downloaded == 0:
        logging.debug("Cannot find url to download")
    return downloaded
