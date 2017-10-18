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
Podcast's generate modules.
"""

from __future__ import unicode_literals
from __future__ import print_function
try:
    # This library should be using by Python2
    import urllib.request as urllib  # pylint: disable=E0611,F0401
except ImportError:
    import urllib
import re

    
def desc_format(text):
    result = text
    result = re.sub(r"[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}", r"<a href='mailto:\g<0>'>\g<0></a>", result)
    result = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", r"<a href='\g<0>'>\g<0></a>", result)
    result = re.sub(r"\/redirect(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", r"<a href='http://youtube.com\g<0>'>\g<0></a>", result)
    result = result.replace("\n", "<br />\n")
    return result


def format_str(text):
    return text.replace("&", "&amp;")


def encode_str(text):
    return urllib.quote(text, safe='')
    

class PodcastItem(object):

    def __init__(self, args, filename, name, url_prefix):
        self.__args = args
        self.__filename = filename
        self.__name = name
        self.__prefix = url_prefix

    def __str__(self):
        return ("<item>\n"
                "<title>{title}</title>\n"
                "<link>{url}</link>\n"
                "<author>{author}</author>\n"
                "<itunes:author>{author}</itunes:author>\n"
                "<description><![CDATA[\n"
                "{description}\n"
                "\n"
                "<p>You Tube: <a href=\"{url}\">{url}</a></p>\n"
                "]]>\n"
                "</description>\n"
                "<enclosure url='{prefix}/{name}/{mp3_url}' type='audio/mpeg'/>\n"
                "<pubDate>{date}</pubDate>\n"
                "</item>\n"
                "").format(title=format_str(self.__args['title']),
                           url=self.__args['url'],
                           author=format_str(self.__args['uploader']),
                           description=desc_format(self.__args['description']),
                           name=self.__name,
                           prefix=self.__prefix,
                           mp3_url=encode_str(self.__filename)+".mp3",
                           date=self.__args['data'])


class Podcast(object):

    def __init__(self, filename, args):
        self.__data = args
        self.__filename = filename
        self.__items = []

    def add_item(self, data, filename, dirname):
        self.__items.append(PodcastItem(data,
                                        filename,
                                        dirname,
                                        url_prefix=self.__data['url_prefix']))

    def generate(self):
        result = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
                  "<rss version=\"2.0\" xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" >\n"
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
