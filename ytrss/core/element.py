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
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import re
import json
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
    """
    def __init__(self, intro):
        """
        Element constructor.

        @param self: object handler
        @type self: L{Element}
        @param intro: Initialization parameter
        @type intro: str | dict
        """
        if isinstance(intro, unicode) or isinstance(intro, str):
            if bool(re.search("^[A-Za-z0-9_\\-]{11}$", intro)):
                self.__code = intro
            elif bool(re.search("^http(s)?://(www.)?youtube.com/watch\\?v="
                                "[A-Za-z0-9_\\-]{11}$", intro)):
                m_result = re.match("http(s)?://(www.)?youtube.com/watch\\?v="
                                    "(?P<code>[A-Za-z0-9_\\-]{11})", intro)
                self.__code = m_result.group('code')
            elif bool(re.search("^http(s)?://youtu.be/[A-Za-z0-9_\\-]"
                                "{11}$", intro)):
                m_result = re.match("http(s)?://youtu.be/(?P<code>[A-Za-z0-9_\\-]"
                                    "{11})", intro)
                self.__code = m_result.group('code')
            elif bool(re.search("^{", intro)) and bool(re.search("}$", intro)):
                try:
                    tab = Element.__from_string(intro)
                    self.__code = tab['code']
                except InvalidStringJSONParseError:
                    raise InvalidParameterElementError("Problem with"
                                                       "parsing json string")
            else:
                raise InvalidParameterElementError("Unknow string [{text}]"
                                                   "".format(text=intro))
        elif isinstance(intro, dict):
            try:
                self.__code = intro['code']
            except KeyError:
                raise InvalidParameterElementError("Invalid dictionary "
                                                   "structure")
        else:
            raise InvalidParameterElementError("Invalid adress: [{url}]"
                                               "".format(url=intro))

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
        if isinstance(other, unicode) or isinstance(other, str):
            if other == "":
                return False
            tmp_other = Element(other)
            return tmp_other == self
        return self.__code == other.code

    def __str__(self):
        """
        Return string from object

        @param self: object handler
        @type self: L{Element}
        @return: string URL
        @rtype: str
        """
        return self.url
