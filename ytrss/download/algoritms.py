"""
Module with algorithms that download files
"""

import logging
import sys
from locks import Mutex

from ytrss.configuration.configuration import Configuration
from ytrss.core.entity.destination import Destination
from ytrss.core.entity.downloader import DownloaderError
from ytrss.core.entity.movie import Movie
from ytrss.core.factory.database_get import create_database_get
from ytrss.core.factory.downloader import create_downloader


def download_movie(configuration: Configuration, movie: Movie, destination: Destination) -> None:
    """
    Download one movie and save it to destination.
    """
    downloader = create_downloader(configuration)
    files = downloader.download(movie)
    destination.save(files)


# pylint: disable=R0915
def download_all_movie(configuration: Configuration) -> int:
    """
    Download all movie saved it to destination.
    """

    logging.info("download movie from urls")
    downloaded = 0
    try:
        with Mutex('/tmp/lock_ytdown', timeout=0.5):
            with create_database_get(configuration) as database:

                for movie_task in database.movies():
                    if not database.is_new(movie_task.movie, movie_task.destination):
                        print(f"URL {movie_task.movie} cannot again download")
                        continue
                    if not movie_task.movie.is_ready:
                        print("movie is not ready to download")
                        database.down_next_time(movie_task.movie, movie_task.destination)
                        continue
                    destination = configuration.conf.destination_manager[movie_task.destination]
                    try:
                        download_movie(configuration, movie_task.movie, destination)
                        print("finish ok")
                        database.add_to_history(movie_task.movie, movie_task.destination)
                        downloaded = downloaded + 1
                    except DownloaderError:
                        print("finish error")
                        database.mark_error(movie_task.movie, movie_task.destination)

    except BlockingIOError:
        print("Program is running.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt by user.")
        sys.exit(1)
    except Exception as ex:
        print(f"Unexpected Error: {type(ex)}")
        raise ex
    if downloaded == 0:
        logging.debug("Cannot find url to download")
    return downloaded
