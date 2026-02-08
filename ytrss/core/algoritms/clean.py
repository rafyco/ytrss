from dataclasses import dataclass
from datetime import datetime
from typing import List, Iterator
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.helpers.logging import logger
from ytrss.core.managers.manager_service import ManagerService, default_manager_service
from ytrss.database.database import DatabaseStatus


@dataclass
class _MovieWithData:
    def __init__(self, movie: DownloadedMovie, date: datetime) -> None:
        self.movie = movie
        self.date = date


def filter_limits(
        manager_service: ManagerService,
        movies: List[DownloadedMovie],
        limit: int = 20
) -> Iterator[DownloadedMovie]:
    """ Return a list of movies that are pass to limits """

    movie_list: List[_MovieWithData] = []

    for movie in movies:
        create_date = manager_service.database.get_created_data(movie)
        if create_date is None:
            yield movie
        else:
            movie_list.append(_MovieWithData(movie, create_date))

    sorted_movies = sorted(movie_list, key=lambda movie_data: movie_data.date)
    yield from map(lambda movie_data: movie_data.movie, sorted_movies[:-limit])


async def clean_tasks(
    manager_service: ManagerService = default_manager_service()
) -> None:
    """ Clean tasks """

    for destination in manager_service.destination_manager.destinations:
        deleted_movies = destination.saved_movies
        deleted_movies = filter_limits(manager_service, list(deleted_movies), limit = destination.info.limit)
        print("Start deleting")
        for movie in deleted_movies:
            logger.info("Movie deleted: [%s] %s",
                        movie.url,
                        movie.title)
            destination.delete(movie, manager_service.templates_manager)
            manager_service.database.change_type(movie, DatabaseStatus.DELETED)
