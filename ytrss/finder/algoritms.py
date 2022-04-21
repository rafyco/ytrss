"""
Algorithms to prepare urls to download from sources.
"""

import logging

from ytrss.configuration.configuration import Configuration
from ytrss.core.factory.database import create_database
from ytrss.finder.url_finder import URLFinder


def prepare_urls(settings: Configuration) -> None:
    """
    Prepare urls for downloader.
    """
    logging.info("Prepare new urls")
    finder = URLFinder(settings.conf.sources)
    queue = create_database(settings)
    for movie_task in finder.movies:
        if queue.queue_mp3(movie_task.movie, movie_task.destination):
            print(f"New element: {movie_task.movie.title} [{movie_task.movie.identity}]"
                  f"destination=[{movie_task.destination}]")
        else:
            logging.info("Element exists: %s", movie_task.movie.url)
