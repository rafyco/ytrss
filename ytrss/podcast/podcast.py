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

import logging
from typing import List, Optional

from ytrss.configuration.entity.podcast_info import PodcastInfo
from ytrss.core.downloaded_movie import DownloadedMovie
from ytrss.podcast.helpers import desc_format, format_str


class _Item:
    """
    Podcast Item builder.

    This class prepare one movie description.
    """

    def __init__(self, movie: DownloadedMovie, name: str, url_prefix: str) -> None:
        self.__desc: Optional[str] = None
        try:
            self.__args = movie.data
            self.__filename = movie.name
            self.__name = name
            self.__prefix = url_prefix
        except ValueError:
            raise ValueError("Cannot create podcast item")

    @property
    def description(self) -> str:
        """ Formatted description of podcast item. """
        if self.__desc is None:
            self.__desc = desc_format(self.__args['description'])
        return self.__desc if self.__desc is not None else ""

    def __get_arg(self, key: str, default: str = "") -> str:
        return self.__args.get(key, default) if self.__args is not None else default

    def __str__(self) -> str:
        logging.debug("item print: %s", self.__args['code'])
        return (f"<item>\n"
                f"<title>{format_str(self.__args.get('title', '<no title>'))}</title>\n"
                f"<image>\n"
                f"<title>cover</title>\n"
                f"<url>{format_str(self.__get_arg('image'))}</url>\n"
                f"</image>\n"
                f"<link>{format_str(self.__get_arg('url'))}</link>\n"
                f"<author>{format_str(self.__get_arg('uploader'))}</author>\n"
                f"<itunes:author>{format_str(self.__get_arg('uploader'))}</itunes:author>\n"
                f"<itunes:image href=\"{self.__get_arg('image')}\"/>\n"
                f"<description><![CDATA[\n"
                f"{self.description}\n"
                f"<br />\n"
                f"<img style=\"width:100%\" src=\"{self.__get_arg('image')}\" />\n"
                f"\n"
                f"<p>Uploader: {format_str(self.__get_arg('uploader'))}</p>\n"
                f"<p>You Tube: <a href=\"{self.__get_arg('url')}\">{format_str(self.__get_arg('url'))}"
                f"</a></p>\n"
                f"<p>Podcast generated by: "
                f"<a href=\"https://ytrss.readthedocs.io/\">ytrss</a></p>\n"
                f"]]>\n"
                f"</description>\n"
                f"<enclosure url='{self.__prefix}/{self.__name}/{self.__filename}.mp3' "
                f"type='audio/mpeg'/>\n"
                f"<pubDate>{self.__get_arg('data')}</pubDate>\n"
                f"</item>\n")


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
        self.__items: List[_Item] = []

    def add_item(self, movie: DownloadedMovie, dir_name: str) -> None:
        """
        Add item to podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @param movie: movie's file
        @type movie: L{Movie<ytrss.core.movie.Movie>}
        @param dir_name: name of directory
        @type dir_name: str
        """
        self.__items.append(_Item(movie,
                                  dir_name,
                                  url_prefix=self.__podcast_info.url_prefix))

    def generate(self) -> str:
        """
        Generate podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @return: source of podcast
        @rtype: str
        """
        result = (f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
                  f"<rss version=\"2.0\" "
                  f"xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd"
                  f"\" >\n"
                  f"<channel>\n"
                  f"<title>{self.__podcast_info.title}</title>\n"
                  f"<itunes:author>{self.__podcast_info.author}</itunes:author>\n"
                  f"<language>{self.__podcast_info.language}</language>\n"
                  f"<link>{self.__podcast_info.link}</link>\n"
                  f"<description>{self.__podcast_info.desc}</description>\n"
                  f"<itunes:summary>{self.__podcast_info.desc}</itunes:summary>\n")
        if self.__podcast_info.img is not None:
            result = (f"{result}"
                      f"<image>\n"
                      f"<title>{self.__podcast_info.title}</title>\n"
                      f"<url>{self.__podcast_info.img}</url>\n"
                      f"<link>{self.__podcast_info.link}</link>\n"
                      f"</image>\n")
        for item in self.__items:
            result = f"{result}\n{item}"
        result = (f"{result}"
                  f"</channel>\n"
                  f"</rss>\n")
        return result

    def __str__(self) -> str:
        return self.generate()
