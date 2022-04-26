from ytrss.controlers.youtube_dl.movie import YouTubeMovie
from ytrss.core.entity.movie import Movie
from ytrss.core.factory import BaseFactory
from ytrss.core.typing import Url


class MovieFactory(BaseFactory[Url, Movie]):

    @classmethod
    def build(cls, param: Url) -> Movie:
        return YouTubeMovie(param)


create_movie = MovieFactory()
