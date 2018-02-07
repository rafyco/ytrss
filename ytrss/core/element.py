#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
#                                                                         #
#  Copyright (C) 2017  Rafal Kobel <rafalkobel@rafyco.pl>                 #
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

from __future__ import unicode_literals
from __future__ import print_function
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import re
import sys
import json
import time
import datetime
from email import utils
import youtube_dl
from ytrss.core.downloader import Downloader


class InvalidStringJSONParseError(Exception):
    """ Element Parse Exception """
    pass


class InvalidParameterElementError(Exception):
    """ Element Exception - Invalid Parameter """
    pass


class Element(object):
    """
    Element to download.

    @ivar url: url YouTube movie
    @type url: str
    @ivar code: code of YouTube movie
    @type code: str
    @ivar title: title of YouTube movie
    @type title: str
    @ivar author: name of uploader
    @type author: str
    @ivar desc: movie's description
    @type desc: str
    @ivar date: movie's create date
    @type data: str
    @ivar img_url: url to thumbnail
    @type img_url: str
    """
    def __init__(self, intro, destination_dir="other"):
        """
        Element constructor.

        @param self: object handler
        @type self: L{Element}
        @param intro: Initialization parameter
        @type intro: str | dict
        """
        self.__title = None
        self.__author = None
        self.__desc = None
        self.__date = None
        self.__img_url = None
        self.__json_data = None
        self.destination_dir = destination_dir
        if isinstance(intro, dict):
            try:
                self.__code = intro['code']
                self.__date = intro['data']
            except KeyError:
                raise InvalidParameterElementError("Invalid dictionary "
                                                   "structure")
        else:
            try:
                if bool(re.search("^[A-Za-z0-9_\\-]{11}$", intro)):
                    self.__code = intro
                elif bool(re.search("^http(s)?://(www.)?youtube.com/watch\\?v="
                                    "[A-Za-z0-9_\\-]{11}$", intro)):
                    m_result = re.match("http(s)?://(www.)?youtube.com/watch\\?"
                                        "v=(?P<code>[A-Za-z0-9_\\-]{11})"
                                        "", intro)
                    self.__code = m_result.group('code')
                elif bool(re.search("^http(s)?://youtu.be/[A-Za-z0-9_\\-]"
                                    "{11}$", intro)):
                    m_result = re.match("http(s)?://youtu.be/(?P<code>"
                                        "[A-Za-z0-9_\\-]{11})", intro)
                    self.__code = m_result.group('code')
                elif bool(re.search("^{", intro)) and bool(re.search("}$",
                                                                     intro)):
                    try:
                        tab = Element.__from_string(intro)
                        self.__code = tab['code']
                        try:
                            self.destination_dir = tab['destination']
                        except KeyError:
                            pass
                    except InvalidStringJSONParseError:
                        raise InvalidParameterElementError("Problem with"
                                                           "parsing "
                                                           "json string")
                else:
                    raise InvalidParameterElementError("Unknow string [{text}]"
                                                       "".format(text=intro))
            except TypeError:
                raise InvalidParameterElementError("Invalid adress type: [{}]"
                                                   "".format(type(intro)))

    @property
    def code(self):
        """
        Movie's ID
        """
        return self.__code

    @property
    def url(self):
        """
        URL to movie
        """
        return "https://www.youtube.com/watch?v={}".format(self.__code)

    def __get_youtube_data(self, option):
        """
        Get JSON data for youtube movie

        @param self: object handler
        @type self: L{Element}
        @param option: name of option to return
        @type option: str
        @return: Value of searching option
        @rtype: str
        """
        if self.__json_data is None:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = tmp_stdout = StringIO()
            sys.stderr = StringIO()
            try:
                command = ["--dump-json", self.url]
                youtube_dl.main(command)
            except SystemExit:
                pass
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            json_output = tmp_stdout.getvalue()
            self.__json_data = json.load(StringIO(json_output))
        return self.__json_data[option]

    @property
    def title(self):
        """
        movie's title
        """
        if self.__title is None:
            self.__title = self.__get_youtube_data("title")
        return self.__title

    @property
    def author(self):
        """
        movie's author
        """
        if self.__author is None:
            self.__author = self.__get_youtube_data('uploader')
        return self.__author

    @property
    def desc(self):
        """
        movie's description
        """
        if self.__desc is None:
            self.__desc = self.__get_youtube_data("description")
        return self.__desc

    @property
    def date(self):
        """
        mvoie's create data
        """
        if self.__date is None:
            now_day = datetime.datetime.now()
            nowtuple = now_day.timetuple()
            nowtimestamp = time.mktime(nowtuple)
            self.__date = utils.formatdate(nowtimestamp)
        return self.__date

    @property
    def img_url(self):
        """
        image's ULR
        """
        if self.__img_url is None:
            self.__img_url = self.__get_youtube_data("thumbnail")
        return self.__img_url

    def download(self, settings):
        """
        Download element

        @param self: object handler
        @type self: L{Element}
        @param settings: setting handler
        @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
        @return: C{True} if download correct, C{False} otherwise
        @rtype: bool
        """
        task = Downloader(settings, self)
        return task.download()

    def to_string(self):
        """
        Make string reprezenting object

        @param self: object handler
        @type self: L{Element}
        @return: JSON's string
        @rtype: str
        """
        tab = dict()
        tab['code'] = self.__code
        tab['destination'] = self.destination_dir
        return json.dumps(tab)

    @staticmethod
    def __from_string(text):
        """
        Set object from JSON string

        @param text: JSON string
        @type text: str
        @return: tab from JSON
        @rtype: str
        """
        try:
            tab = json.load(StringIO(text))
        except ValueError:
            raise InvalidStringJSONParseError("Cannot prepare string")
        return tab

    def __eq__(self, other):
        """
        Compare object with another object

        @param self: object handler
        @type self: L{Element}
        @param other: other object handler or URL string
        @type other: L{Element} or str
        @return: C{True} if object equal, C{False} otherwise
        @rtype: bool
        """
        if isinstance(other, Element):
            return self.__code == other.code
        else:
            if other == "":
                return False
            tmp_other = Element(other)
            return tmp_other == self

    def get_json_description(self):
        """
        Retrun movie's description in JSON format

        @return: movie's description
        @rtype: str
        """
        result = {
            'url': self.url,
            'code': self.code,
            'title': self.title,
            'uploader': self.author,
            'description': self.desc,
            'image': self.img_url,
            'data': self.date
        }
        return json.dumps(result)

    def __str__(self):
        """
        Return string from object

        @param self: object handler
        @type self: L{Element}
        @return: string URL
        @rtype: str
        """
        return self.url
