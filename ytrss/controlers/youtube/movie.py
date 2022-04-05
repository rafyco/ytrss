#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2021 Rafal Kobel <rafalkobel@rafyco.pl>             #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################
"""
Element to download
"""
import copy
from json import JSONDecodeError
from typing import Dict, Any, Optional

import sys
import json
import time
import datetime
from io import StringIO
from email import utils
import youtube_dl
from ytrss.configuration.configuration import Configuration
from ytrss.configuration.consts import DEFAULT_PODCAST_DIR
from ytrss.core.entity.movie import Movie, InvalidParameterMovieError
from ytrss.controlers.youtube.youtube_downloader import YouTubeDownloader


class YouTubeMovie(Movie):
    """
    Movie's data.
    """

    def __init__(self, url: str, destination_dir: str = DEFAULT_PODCAST_DIR) -> None:
        """
        Element constructor.

        @param self: object handler
        @type self: L{Movie}
        """
        self.destination_dir = destination_dir
        self._url = url

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
    def url(self) -> str:
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
    def date(self) -> str:
        """
        movie's create data
        """
        now_day = datetime.datetime.now()
        nowtuple = now_day.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        return utils.formatdate(nowtimestamp)

    @property
    def img_url(self) -> Optional[str]:
        """
        image's ULR
        """
        img = self.__get_youtube_data("thumbnail")
        return img if img != "" else None

    @property
    def is_ready(self) -> bool:
        """
        Is movie is ready to download
        """
        is_live = "false"
        if self._error is None:
            is_live = self.__get_youtube_data("is_live")

        return ("Premieres in" not in self._error if self._error is not None else True) and is_live.lower() != "true"

    def download(self, settings: Configuration) -> bool:
        """
        Download element
        """
        return YouTubeDownloader(settings).download(self.identity, self.url, self.destination_dir, self.json)

    def to_string(self) -> str:
        """
        Make string representing object

        @param self: object handler
        @type self: L{Movie}
        @return: JSON's string
        @rtype: str
        """
        tab = dict()
        tab['id'] = self.identity
        tab['destination'] = self.destination_dir
        tab['url'] = self.url
        return json.dumps(tab)

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
            'date': self.date
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
