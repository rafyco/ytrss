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
Settings parser module.

File are read from the first of the following location.

For MS Windows

    - I{~/YTRSS/config}

For Linux (and other systems)

    - I{/etc/ytrss/config}
    - I{~/.config/ytrss/config}

In some case you can set file path in constructor or read data in json format.

Config file structure
=====================

Configuration file is in a json format with following option:

    - I{output} - Path to folder where program should download files.
    - I{subscription} - List of subscription.
        For more see: L{parsing function
        <ytrss.core.settings.YTSettings.__parse_subsctiptions>}
    - I{arguments} - (optional) List of argument for C{youtube_dl} script
    - I{podcasts} - (optional) Dictionary of directory settings
        where key is dir name.
        For more see: L{rss generator
        <ytrss.core.settings.YTSettings.get_podcast_information>}

Example file
============

code of example file::

    {
        "output"   : "<output_file>",
        "subscriptions" : [
            {
                "code"    : "<playlist_id>",
                "type"    : "playlist"
            },
            {
                "code"    : "<subscription_id>"
            },
            {
                "code"    : "<subscription_id>",
                "enabled" : false
            }
        ]
    }

"""
from typing import Optional, Dict, Sequence
from typing import List, Any
import os
import sys

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.podcast_info import PodcastInfo
from ytrss.configuration.entity.source import Source


class DataConfiguration(Configuration):
    """
    Parser settings for ytrss.

    Class read settings from parameters or from default conf file.
    """

    @property
    def cache_path(self) -> str:
        return self.__cache_path

    @property
    def args(self) -> List[str]:
        return self.__args

    @property
    def output(self) -> str:
        return self.__output

    @property
    def sources(self) -> Sequence[Source]:
        return self.__sources

    @property
    def config_path(self) -> str:
        return self.__conf_path

    # pylint: disable=R0912,R0915
    def __init__(self, conf_data: Dict[str, Any]) -> None:
        """
        YTSettings constructor.

        @param self: object handle
        @param conf_data: Dictionary with configuration

        @raise SettingException: In case of C{conf_file} and C{conf_str}
            are not set.
        """

        if 'config_dir' in conf_data:
            self.__conf_path = os.path.expanduser(conf_data['config_dir'])
        else:
            if sys.platform.lower().startswith('win'):
                conf_path = os.path.join("~\\YTRSS")
            else:
                conf_path = os.path.join("~/.config/ytrss")
            self.__conf_path = os.path.expanduser(conf_path)

        try:
            os.makedirs(self.__conf_path)
        except OSError:
            pass

        self.__cache_path = os.path.join(self.__conf_path, "cache")

        self.__output: str = "~/ytrss"
        if 'output' in conf_data:
            self.__output = os.path.expanduser(conf_data.get('output'))
            try:
                os.makedirs(self.__output)
            except OSError:
                pass

        self.__args: List[str] = []
        if 'arguments' in conf_data:
            if isinstance(conf_data['arguments'], list):
                self.__args = conf_data['arguments']
            else:
                self.__args = [conf_data['arguments']]

        self.__sources: List[Source] = []
        if 'subscriptions' in conf_data and isinstance(conf_data['subscriptions'], list):
            for subscription in conf_data['subscriptions']:
                source = Source.from_json(subscription)
                if source.enable:
                    self.__sources.append(source)

        self.__podcast: Optional[Dict[str, Any]] = None
        if 'podcasts' in conf_data and 'outputs' in conf_data['podcasts']:
            self.__podcast = conf_data['podcasts']['outputs']

    @staticmethod
    def __print_url_name(elem: Source) -> str:
        """
        Print information from dictionary

        @param elem: url information
        @return: formatted name of url
        """
        return f"{elem.name} ({elem.code})"

    def __str__(self) -> str:
        """
        Display settings information.

        @param self: object handle
        @return: formatted configuration
        """
        result = "Youtube configuration:\n\n"
        result += f"output-file: {self.output}\n"
        for elem in self.__sources:
            result += f"\t{elem.type}: %s\n" % self.__print_url_name(elem)
        return result

    def get_podcast_information(self, folder_name: str) -> PodcastInfo:
        """
        Return podcast information from json files

        Information is dictionary of objects with following fields:

            - I{title} - Name of podcast
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

        @param self: object handle
        @type self: L{Configuration}
        @param folder_name: name of rendering directory
        @type folder_name: src
        @return: data of rendering directory
        @rtype: dict
        """
        result = PodcastInfo.from_json(
            self.__podcast.get(folder_name, None) if self.__podcast is not None else None
        )

        result.url_prefix = \
            self.__podcast.get('url_prefix', "") if self.__podcast is not None else ""

        return result
