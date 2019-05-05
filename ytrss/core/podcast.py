#!/usr/bin/env python3
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
Podcast's generate modules.

This class prepare source for rss file. It can by configure by dictionary
set as argument in constructor.
"""

from __future__ import unicode_literals
from __future__ import print_function
try:
    # This library should be using by Python2
    import urllib.request as urllib  # pylint: disable=E0611,F0401
except ImportError:
    import urllib
import logging
import re


def desc_format(text):
    """
    Format description.

    This function replace ulr and newline chars by following html code.
    It is using in rss file to format description in rss reader.

    @param text: Non-formated description
    @type text: str
    @return: HTML formated string
    @rtype: str
    """
    result = text
    result = re.sub(r"[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}",
                    r"<a href='mailto:\g<0>'>\g<0></a>",
                    result)
    result = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|i"
                    "(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                    r"<a href='\g<0>'>\g<0></a>",
                    result)
    result = re.sub(r"\/redirect(?:[a-zA-Z0-9$-_@.&!*\(\)]*)(?:q=(?P<url>[A-Za-z0-9%.]+))+"
                    "(?:[a-zA-Z0-9$-_@.&!*,]*)",
                    r"<a href='\g<url>'>\g<url></a>",
                    result)
    result = re.sub(r"\/(?:redirect|watch)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
                    "(?:%[0-9a-zA-Z][0-9a-zA-Z]))+",
                    r"<a href='https://youtube.com\g<0>'>\g<0></a>",
                    result)
    result = result.replace("\n", "<br />\n")
    result = result.replace("%3A", ":")
    result = result.replace("%2F", "/")
    return result


def format_str(text):
    """
    Format some strings.

    This function replacing invalid chars in xml file.
    ex. RSS does't accept C{&} char so it should be replaced to C{&amp;}

    @param text: Text to formating
    @type text: str
    @return: formated text
    @rtype: str
    """
    return text.replace("&", "&amp;")


def encode_str(text):
    """
    Encode string.

    @param text: string to encode
    @type text: str
    @return: encoded string
    @rtype: str
    """
    return urllib.quote(text.encode("utf8"), safe='')


class PodcastItem(object):
    """
    Podcast Item budilder.

    This class prepare one movie description.
    """

    def __init__(self, movie, name, url_prefix):
        self.__desc = None
        try:
            self.__args = movie.data
            self.__filename = movie.name
            self.__name = name
            self.__prefix = url_prefix
        except ValueError:
            raise ValueError("Cannot create podcast item")

    @property
    def description(self):
        """ Formated description of podcast item. """
        if self.__desc is None:
            self.__desc = desc_format(self.__args['description'])
        return self.__desc

    def __str__(self):
        logging.debug("item print: %s", self.__args['code'])
        return ("<item>\n"
                "<title>{title}</title>\n"
                "<image>\n"
                "<title>cover</title>\n"
                "<url>{img}</url>\n"
                "</image>\n"
                "<link>{url}</link>\n"
                "<author>{author}</author>\n"
                "<itunes:author>{author}</itunes:author>\n"
                "<description><![CDATA[\n"
                "{description}\n"
                "<img style=\"width:100%\" src=\"{img}\" />\n"
                "\n"
                "<p>Uploader: {author}</p>\n"
                "<p>You Tube: <a href=\"{url}\">{url}</a></p>\n"
                "<p>Podcast generated by: "
                "<a href=\"https://ytrss.readthedocs.io/\">ytrss</a></p>\n"
                "]]>\n"
                "</description>\n"
                "<enclosure url='{prefix}/{name}/{mp3_url}' "
                "type='audio/mpeg'/>\n"
                "<pubDate>{date}</pubDate>\n"
                "</item>\n"
                "").format(title=format_str(self.__args['title']),
                           url=self.__args['url'],
                           author=format_str(self.__args['uploader']),
                           description=self.description,
                           img=self.__args['image'],
                           name=self.__name,
                           prefix=self.__prefix,
                           mp3_url=encode_str(self.__filename) + ".mp3",
                           date=self.__args['data'])


class Podcast(object):
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

    def __init__(self, filename, args):
        """
        Object constructor.

        @param self: object handle
        @type self: L{Podcast}
        @param filename: path to movies
        @type filename: str
        @param args: Dictionary of args described
            L{here<ytrss.core.podcast.Podcast>}
        @type args: dict
        """
        self.__data = args
        self.__filename = filename
        self.__items = []

    @property
    def limit(self):
        """
        Limit of displayed files.
        """
        if 'limit' not in self.__data:
            return 100
        return self.__data['limit']

    def add_item(self, movie, dirname):
        """
        Add item to podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @param movie: movie's file
        @type movie: L{Movie<ytrss.core.movie.Movie>}
        @param dirname: name of directory
        @type dirname: str
        """
        self.__items.append(PodcastItem(movie,
                                        dirname,
                                        url_prefix=self.__data['url_prefix']))

    def generate(self):
        """
        Generate podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @return: source of podcast
        @rtype: str
        """
        result = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
                  "<rss version=\"2.0\" "
                  "xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd"
                  "\" >\n"
                  "<channel>\n"
                  "<title>{title}</title>\n"
                  "<itunes:author>{author}</itunes:author>\n"
                  "<language>{language}</language>\n"
                  "<link>{link}</link>\n"
                  "<description>{desc}</description>\n"
                  "<itunes:summary>{desc}</itunes:summary>\n"
                  "").format(title=format_str(self.__data['title']),
                             author=format_str(self.__data['author']),
                             language=self.__data['language'],
                             link=self.__data['link'],
                             desc=self.__data['desc'])
        if 'img' in self.__data and self.__data['img'] != "":
            result = ("{result}"
                      "<image>\n"
                      "<title>{title}</title>\n"
                      "<url>{img}</url>\n"
                      "<link>{link}</link>\n"
                      "</image>\n"
                      "").format(result=result,
                                 title=self.__data['title'],
                                 img=self.__data['img'],
                                 link=self.__data['link'])
        for elem in self.__items:
            result = "{}\n{}".format(result, elem)
        result = ("{result}"
                  "</channel>\n"
                  "</rss>\n"
                  "").format(result=result)
        return result

    def __str__(self):
        return self.generate()
