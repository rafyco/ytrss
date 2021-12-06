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
from typing import Union, Dict, Any, Optional

import re
import sys
import json
import time
import datetime
from io import StringIO
from email import utils
import youtube_dl
from ytrss.configuration.configuration import Configuration

from ytrss.core.downloader import Downloader


class InvalidStringJSONParseError(Exception):
    """ Element Parse Exception """


class InvalidParameterMovieError(Exception):
    """ Element Exception - Invalid Parameter """


class Movie:
    """
    Movie's data.
    """

    def __init__(self, arg: Union[str, Dict[str, Any]], destination_dir: str = "other") -> None:
        """
        Element constructor.

        @param self: object handler
        @type self: L{Movie}
        """
        self.__title: Optional[str] = None
        self.__author: Optional[str] = None
        self.__desc: Optional[str] = None
        self.__date: Optional[str] = None
        self.__img_url: Optional[str] = None
        self.__json_data: Optional[Dict[str, str]] = None
        self.__code: Optional[str] = None
        self.__error: Optional[str] = None
        self.destination_dir = destination_dir
        if isinstance(arg, dict):
            try:
                self.__code = arg['code']
                self.__date = arg['data']
            except KeyError:
                raise InvalidParameterMovieError("Invalid dictionary "
                                                 "structure")
        else:
            try:
                if bool(re.search("^[A-Za-z0-9_\\-]{11}$", arg)):
                    self.__code = arg
                elif bool(re.search("^http(s)?://(www.)?youtube.com/watch\\?v="
                                    "[A-Za-z0-9_\\-]{11}$", arg)):
                    m_result = re.match("http(s)?://(www.)?youtube.com/watch\\?"
                                        "v=(?P<code>[A-Za-z0-9_\\-]{11})"
                                        "", arg)
                    self.__code = m_result.group('code') if m_result is not None else None
                elif bool(re.search("^http(s)?://youtu.be/[A-Za-z0-9_\\-]"
                                    "{11}$", arg)):
                    m_result = re.match("http(s)?://youtu.be/(?P<code>"
                                        "[A-Za-z0-9_\\-]{11})", arg)
                    self.__code = m_result.group('code') if m_result is not None else None
                elif bool(re.search("^{", arg)) and bool(re.search("}$",
                                                                   arg)):
                    try:
                        tab = Movie.__from_string(arg)
                        self.__code = tab['code']
                        try:
                            self.destination_dir = tab['destination']
                        except KeyError:
                            pass
                    except InvalidStringJSONParseError:
                        raise InvalidParameterMovieError("Problem with"
                                                         "parsing "
                                                         "json string")
                else:
                    raise InvalidParameterMovieError("Unknown string [{text}]"
                                                     "".format(text=arg))
            except TypeError:
                raise InvalidParameterMovieError("Invalid address type: [{}]"
                                                 "".format(type(arg)))

    @property
    def code(self) -> str:
        """
        Movie's ID
        """
        return self.__code if self.__code is not None else ""

    @property
    def url(self) -> str:
        """
        URL to movie
        """
        return "https://www.youtube.com/watch?v={}".format(self.__code)

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
        if self.__json_data is None:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = tmp_stdout = StringIO()
            sys.stderr = tmp_stderr = StringIO()
            try:
                youtube_dl.main(['--dump-json', self.url])
            except SystemExit:
                pass
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            json_output = tmp_stdout.getvalue()
            self.__error = tmp_stderr.getvalue()
            try:
                self.__json_data = json.load(StringIO(json_output))
            except JSONDecodeError:
                return ""
        return self.__json_data.get(key, "").__str__()

    @property
    def title(self) -> str:
        """
        movie's title
        """
        if self.__title is None:
            self.__title = self.__get_youtube_data("title")
        return self.__title

    @property
    def author(self) -> str:
        """
        movie's author
        """
        if self.__author is None:
            self.__author = self.__get_youtube_data('uploader')
            return self.__author
        return self.__author

    @property
    def desc(self) -> str:
        """
        movie's description
        """
        if self.__desc is None:
            self.__desc = self.__get_youtube_data("description")
            return self.__desc
        return self.__desc

    @property
    def date(self) -> str:
        """
        movie's create data
        """
        if self.__date is None:
            now_day = datetime.datetime.now()
            nowtuple = now_day.timetuple()
            nowtimestamp = time.mktime(nowtuple)
            self.__date = utils.formatdate(nowtimestamp)
        return self.__date

    @property
    def img_url(self) -> Optional[str]:
        """
        image's ULR
        """
        if self.__img_url is None:
            self.__img_url = self.__get_youtube_data("thumbnail")
        return self.__img_url if self.__img_url != "" else None

    @property
    def is_ready(self) -> bool:
        """
        Is movie is ready to download
        """
        is_live = "false"
        if self.__error is None:
            is_live = self.__get_youtube_data("is_live")

        return ("Premieres in" not in self.__error if self.__error is not None else True) and is_live.lower() != "true"

    def download(self, settings: Configuration) -> bool:
        """
        Download element
        """
        return Downloader(settings).download(self.code, self.url, self.destination_dir, self.json)

    def to_string(self) -> str:
        """
        Make string representing object

        @param self: object handler
        @type self: L{Movie}
        @return: JSON's string
        @rtype: str
        """
        tab = dict()
        tab['code'] = self.__code
        tab['destination'] = self.destination_dir
        return json.dumps(tab)

    @staticmethod
    def __from_string(text: str) -> Dict[str, Any]:
        """
        Set object from JSON string

        @param text: JSON string
        @type text: str
        @return: tab from JSON
        @rtype: str
        """
        try:
            result: Dict[str, Any] = json.load(StringIO(text))
            return result
        except ValueError:
            raise InvalidStringJSONParseError("Cannot prepare string")

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
            return self.__code == other.code
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
            'code': self.code,
            'title': self.title,
            'uploader': self.author,
            'description': self.desc,
            'image': self.img_url,
            'data': self.date
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
