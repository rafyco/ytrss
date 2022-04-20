
from ytrss.controlers.youtube_dl.movie import YouTubeMovie
from ytrss.core.entity.movie import Movie
from ytrss.core.typing import Url


def create_movie(url: Url) -> Movie:
    """
    Create Movie object from args
    """
    return YouTubeMovie(url)
