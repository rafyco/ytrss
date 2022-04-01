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
Module with podcast information object
"""
from typing import Optional, Dict, Any


class PodcastInfo:
    """
    Podcast information object

    The object contains information obout the header of podcast.
    """

    def __init__(self) -> None:
        self.title: str = "unknown title"
        self.author: str = "Nobody"
        self.language: str = "pl-pl"
        self.link: str = "http://youtube.com"
        self.desc: str = "No description"
        self.url_prefix: str = ""
        self.img: Optional[str] = None

    @staticmethod
    def from_json(json: Optional[Dict[str, Any]]) -> 'PodcastInfo':
        """
        Create podcast information object from dictionary
        """
        podcast = PodcastInfo()
        if json is not None:
            if 'title' in json and isinstance(json['title'], str):
                podcast.title = json['title']
            if 'author' in json and isinstance(json['author'], str):
                podcast.author = json['author']
            if 'language' in json and isinstance(json['language'], str):
                podcast.language = json['language']
            if 'link' in json and isinstance(json['link'], str):
                podcast.link = json['link']
            if 'desc' in json and isinstance(json['desc'], str):
                podcast.desc = json['desc']
            if 'url_prefix' in json and isinstance(json['url_prefix'], str):
                podcast.url_prefix = json['url_prefix']
            if 'img' in json and isinstance(json['img'], str):
                podcast.img = json['img']
        return podcast
