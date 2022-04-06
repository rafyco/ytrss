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
Podcast's source builder modules.

This class prepare source for rss file. It can be configured by dictionary
set as argument in constructor.
"""
import os.path
from typing import List
from jinja2 import Environment, FileSystemLoader

import ytrss
from ytrss.configuration.entity.podcast_info import PodcastInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.podcast.helpers import format_str, format_desc, format_date


class Podcast:
    """
    Podcast builder.

    Class makes source for rss file. It can be customizable by specyfic args
    defined in constructor.

    Argument dictionary should have following fields:

        - I{title} - Name of podcastv
            (C{"unknown title"} is default)
        - I{author} - Name of podcast author
            (C{"Nobody"} is default)
        - I{language} - Language of podcast
            (C{"pl-pl"} is default)
        - I{link} - Link to website
            (C{"http://youtube.com"} is default)
        - I{desc} - Description of source
            (C{"No description"} is default)
        - I{url_prefix} - Prefix for movie's url
            (C{""} is default)
        - I{img} - Image of movie
            (C{None} is default)
    """

    def __init__(self, filename: str, podcast_info: PodcastInfo) -> None:
        """
        Object constructor.

        @param self: object handle
        @type self: L{Podcast}
        @param filename: path to movies
        @type filename: str
        @param podcast_info: Dictionary of args described
            L{here<ytrss.core.podcast.Podcast>}
        @type podcast_info: dict
        """
        self.__podcast_info = podcast_info
        self.__filename = filename
        self.__items: List[DownloadedMovie] = []

    def add_item(self, movie: DownloadedMovie) -> None:
        """
        Add item to podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @param movie: movie's file
        @type movie: L{Movie<ytrss.core.movie.Movie>}
        """
        self.__items.append(movie)

    def generate(self) -> str:
        """
        Generate podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @return: source of podcast
        @rtype: str
        """
        env = Environment(
            loader=FileSystemLoader(os.path.join(ytrss.__path__[0], "templates")),  # type: ignore
        )
        env.filters["format_str"] = format_str
        env.filters["format_desc"] = format_desc
        env.filters["format_date"] = format_date

        template = env.get_template("podcast.xml")
        return template.render(podcast_info=self.__podcast_info, dirname=self.__filename, movies=self.__items)

    def __str__(self) -> str:
        return self.generate()
