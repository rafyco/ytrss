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
                "code"    : "<subscritpion_id>"
            },
            {
                "code"    : "<subscription_id>",
                "enabled" : false
            }
        ]
    }

"""
import abc
from typing import Sequence, List

from ytrss.configuration.entity.podcast_info import PodcastInfo
from ytrss.configuration.entity.source import Source


class ConfigurationError(Exception):
    """ Configuration error. """


class Configuration(metaclass=abc.ABCMeta):
    """
    Default settings for ytrss.

    Abstract configuration object. It has a configuration information.
    """

    @property
    @abc.abstractmethod
    def output(self) -> str:
        """ Path to directory, where podcast files should be saved. """

    @property
    @abc.abstractmethod
    def sources(self) -> Sequence[Source]:
        """ A list of sources """

    @property
    @abc.abstractmethod
    def config_path(self) -> str:
        """ Path to directory with databases. """

    @property
    @abc.abstractmethod
    def cache_path(self) -> str:
        """ Path to directory where the file can be placed before the download will be finished. """

    @property
    @abc.abstractmethod
    def args(self) -> List[str]:
        """ Arguments for youtube_dl. """

    @abc.abstractmethod
    def get_podcast_information(self, folder_name: str) -> PodcastInfo:
        """ Return information about podcast. """
