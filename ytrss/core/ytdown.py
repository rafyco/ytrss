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

from __future__ import unicode_literals
import abc
import logging
from urllib import urlopen
from xml.dom import minidom


class YTDown(object):
    """ Klasa do pobierania listy adresow url filmow z podanego zrodla. """

    __metaclass__ = abc.ABCMeta

    def __init__(self, code, link_type='user'):
        self.code = code
        self.link_type = link_type

    def __build_url(self):
        patern = "channel_id"
        if self.link_type == 'playlist':
            patern = "playlist_id"
        return "https://www.youtube.com/feeds/videos.xml?{}={}".format(patern, self.code)

    @staticmethod
    def __youtube_list_from_address(address):
        """ Zwraca liste filmow dla uzytkownika o podanym adresie. """
        xml_str = urlopen(address).read()
        xmldoc = minidom.parseString(xml_str)
        tags = xmldoc.getElementsByTagName('link')
        result = []
        iterator = 0
        for elem in tags:
            if iterator != 0 and iterator != 1:
                url = elem.getAttribute("href")
                result.append(url)
            iterator = iterator + 1
        return result

    def get_urls(self):
        url = self.__build_url()
        logging.debug("URL: %s", url)
        return YTDown.__youtube_list_from_address(url)
