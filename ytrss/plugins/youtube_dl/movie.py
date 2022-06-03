import copy
from json import JSONDecodeError
from typing import Optional

import sys
import json
from datetime import datetime
from io import StringIO
import youtube_dl

from ytrss.core.entity.movie import Movie, MovieError
from ytrss.core.helpers.typing import Url


class InvalidDataMovieError(MovieError):
    """ Invalid parameter movie error

    This exception is invoked when the movie data is invalid
    """


class YouTubeMovie(Movie):
    """ A YouTube implementation of movie """

    def __init__(self, url: Url) -> None:
        self._url: Url = url
        self._date: Optional[datetime] = None

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = tmp_stdout = StringIO()
        sys.stderr = tmp_stderr = StringIO()
        try:
            youtube_dl.main(['--dump-json', url])
        except SystemExit:
            pass
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        json_output = tmp_stdout.getvalue()
        self._error = tmp_stderr.getvalue()
        self._json_data = {}
        try:
            self._json_data = json.load(StringIO(json_output))
        except JSONDecodeError as exc:
            raise InvalidDataMovieError(f"Invalid address type: [{url}] -> {self._error}") from exc

    @property
    def url(self) -> Url:
        return self._url

    @property
    def identity(self) -> str:
        extractor: str = self.__get_youtube_data("extractor")
        code: str = self.__get_youtube_data("display_id")
        return f"ytdl:{extractor}:{code}"

    def __get_youtube_data(self, key: str) -> str:
        return str(self._json_data.get(key, ""))

    @property
    def title(self) -> str:
        return self.__get_youtube_data("title")

    @property
    def author(self) -> str:
        return self.__get_youtube_data('uploader')

    @property
    def description(self) -> str:
        return self.__get_youtube_data("description")

    @property
    def date(self) -> datetime:
        try:
            return datetime.strptime(self.__get_youtube_data("upload_date"), "%Y%m%d")
        except ValueError:
            return datetime.now()

    @property
    def img_url(self) -> Optional[Url]:
        img = self.__get_youtube_data("thumbnail")
        return Url(img) if img != "" else None

    @property
    def is_ready(self) -> bool:
        is_live = "false"
        if self._error is None:
            is_live = self.__get_youtube_data("is_live")

        return ("Premieres in" not in self._error if self._error is not None else True) and is_live.lower() != "true"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Movie):
            return self.identity == other.identity
        if other == "":
            return False
        tmp_other = copy.deepcopy(other)
        return tmp_other == self

    def __str__(self) -> str:
        return self.url
