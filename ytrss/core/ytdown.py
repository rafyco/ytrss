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
from ytrss.core.sys.debug import Debug
from urllib import urlopen
from xml.dom import minidom
import abc

class YTDown:
    """ Klasa do pobierania listy adresow url filmow z podanego zrodla. """
    __metaclass__ = abc.ABCMeta
    def __init__(self, code, type='user'):
        self.code = code
        self.type = type

    def build_url(self):
        if self.type == 'playlist':
            return "https://www.youtube.com/feeds/videos.xml?playlist_id={}".format(self.code)
        else:
            return "https://www.youtube.com/feeds/videos.xml?channel_id={}".format(self.code)
        
    def getUrls(self):
        url = self.build_url()
        Debug().debug_log("URL: %s" % url)
        return self.youtube_list_from_address(url)

    def youtube_list_from_address(self, address):
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
