"""
Command line program to checking movie's URL in subscription.

Program checking subscription and playlist from config and save it
to downloading file. It's recomended to add this file to crontab or call
it manually.

Example usage
=============

To invoke program type in your console::

    python -m ytrss.subs

for more option call program with flag C{--help}
"""

import logging

from ytrss.configuration.configuration import Configuration
from ytrss.core.factory.database_put import create_database_put
from ytrss.finder.url_finder import URLFinder


def prepare_urls(settings: Configuration) -> None:
    """
    Prepare urls for downloader.
    """
    logging.info("Prepare new urls")
    finder = URLFinder(settings.conf.sources)
    queue = create_database_put(settings)
    for movie_task in finder.movies:
        if queue.queue_mp3(movie_task.movie, movie_task.destination):
            print(f"Nowy element: {movie_task.movie.title} [{movie_task.movie.identity}]"
                  "dest=[{movie_task.destination}]")
        else:
            logging.info("Element istnieje: %s", movie_task.movie.url)
