from datetime import datetime
from typing import Optional

from ytrss.core.entity.movie import Movie
from ytrss.core.helpers.typing import Url


class PolskieRadioMovie(Movie):

    def __init__(self, url: Url) -> None:
        self._url = url
        self._id = url

    @property
    def identity(self) -> str:
        return f"prpl:{self._id}"

    @property
    def url(self) -> Url:
        return self.url

    @property
    def title(self) -> str:
        pass

    @property
    def author(self) -> str:
        pass

    @property
    def description(self) -> str:
        pass

    @property
    def date(self) -> datetime:
        pass

    @property
    def img_url(self) -> Optional[Url]:
        pass

    @property
    def is_ready(self) -> bool:
        return True
