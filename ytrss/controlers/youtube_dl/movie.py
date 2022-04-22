"""
Element to download
"""
import copy
from email import utils
from json import JSONDecodeError
from typing import Dict, Any, Optional

import sys
import json
import time
from datetime import datetime
from io import StringIO
import youtube_dl

from ytrss.core.entity.movie import Movie, InvalidParameterMovieError
from ytrss.core.typing import Url


class YouTubeMovie(Movie):
    """
    Movie's data.
    """

    def __init__(self, url: Url) -> None:
        """
        Element constructor.

        @param self: object handler
        @type self: L{Movie}
        """
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
        except JSONDecodeError:
            raise InvalidParameterMovieError(f"Invalid address type: [{url}] -> {self._error}")

    @property
    def url(self) -> Url:
        """
        Movie's url
        """
        return self._url

    @property
    def identity(self) -> str:
        """
        Movie's ID
        """
        extractor: str = self.__get_youtube_data("extractor")
        code: str = self.__get_youtube_data("display_id")
        return f"ytdl:{extractor}:{code}"

    def __get_youtube_data(self, key: str) -> str:
        """
        Get JSON data for youtube movie

        @param self: object handler
        @type self: L{Movie}
        @param key: name of option to return
        @type key: str
        @return: Value of searching option
        @rtype: str
        """
        return str(self._json_data.get(key, ""))

    @property
    def title(self) -> str:
        """
        movie's title
        """
        return self.__get_youtube_data("title")

    @property
    def author(self) -> str:
        """
        movie's author
        """
        return self.__get_youtube_data('uploader')

    @property
    def desc(self) -> str:
        """
        movie's description
        """
        return self.__get_youtube_data("description")

    @property
    def date(self) -> datetime:
        """
        movie's create data
        """
        try:
            return datetime.strptime(self.__get_youtube_data("upload_date"), "%Y%m%d")
        except ValueError:
            return datetime.now()

    @property
    def img_url(self) -> Optional[Url]:
        """
        image's ULR
        """
        img = self.__get_youtube_data("thumbnail")
        return Url(img) if img != "" else None

    @property
    def is_ready(self) -> bool:
        """
        Is movie is ready to download
        """
        is_live = "false"
        if self._error is None:
            is_live = self.__get_youtube_data("is_live")

        return ("Premieres in" not in self._error if self._error is not None else True) and is_live.lower() != "true"

    def __eq__(self, other: object) -> bool:
        """
        Compare object with another object

        @param self: object handler
        @type self: L{Movie}
        @param other: other object handler or URL string
        @type other: L{Movie} or str
        @return: C{True} if object equal, C{False} otherwise
        @rtype: bool
        """
        if isinstance(other, Movie):
            return self.identity == other.identity
        if other == "":
            return False
        tmp_other = copy.deepcopy(other)
        return tmp_other == self

    @property
    def json(self) -> Dict[str, Any]:
        """
        Return movie's description in JSON format
        """
        return {
            'url': self.url,
            'id': self.identity,
            'title': self.title,
            'uploader': self.author,
            'description': self.desc,
            'image': self.img_url,
            'date': utils.formatdate(time.mktime(self.date.timetuple()))
        }

    def __str__(self) -> str:
        """
        Return string from object

        @param self: object handler
        @type self: L{Movie}
        @return: string URL
        @rtype: str
        """
        return self.url
