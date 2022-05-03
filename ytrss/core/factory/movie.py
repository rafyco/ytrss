from typing import Sequence, Callable, Optional

from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.core.entity.movie import Movie
from ytrss.core.factory import BaseFactory
from ytrss.core.helpers.typing import Url


class MovieFactory(BaseFactory[Url, Movie]):

    @property
    def plugins(self) -> Sequence[Callable[[Url], Optional[Movie]]]:
        return [
            YouTubeMovie
        ]


create_movie = MovieFactory()
