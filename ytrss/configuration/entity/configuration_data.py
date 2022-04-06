#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2022 Rafal Kobel <rafalkobel@rafyco.pl>             #
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
import abc
import os
import sys

from typing import Any, List, Optional, Dict, Sequence

from ytrss.configuration.entity.podcast_info import PodcastInfo
from ytrss.configuration.entity.source import Source


class ConfigurationData(metaclass=abc.ABCMeta):
    """ Configuration data. """

    # pylint: disable=R0912,R0915
    def __init__(self) -> None:
        """
        Configuration data constructor.
        """
        self.podcast: Optional[Dict[str, Any]] = None
        self.output: str = ""
        self.sources: Sequence[Source] = []
        self.config_path: str = ""
        self.cache_path: str = ""
        self.args: List[str] = []

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'ConfigurationData':
        """
        Create configuration data object from dictionary
        """

        config_data = ConfigurationData()

        if 'config_dir' in json:
            config_data.config_path = os.path.expanduser(json['config_dir'])
        else:
            if sys.platform.lower().startswith('win'):
                conf_path = os.path.join("~\\YTRSS")
            else:
                conf_path = os.path.join("~/.config/ytrss")
            config_data.config_path = os.path.expanduser(conf_path)

        try:
            os.makedirs(config_data.config_path)
        except OSError:
            pass

        config_data.cache_path = os.path.join(config_data.config_path, "cache")

        config_data.output = os.path.expanduser("~/ytrss")
        if 'output' in json and isinstance(json['output'], str):
            config_data.output = os.path.expanduser(json['output'])
            try:
                os.makedirs(config_data.output)
            except OSError:
                pass

        if 'arguments' in json:
            if isinstance(json['arguments'], list):
                config_data.args = json['arguments']
            else:
                config_data.args = [json['arguments']]

        config_data.sources = []
        if 'subscriptions' in json and isinstance(json['subscriptions'], list):
            for subscription in json['subscriptions']:
                source = Source.from_json(subscription)
                if source.enable:
                    config_data.sources.append(source)

        if 'podcasts' in json and 'outputs' in json['podcasts']:
            config_data.podcast = json['podcasts']['outputs']

        return config_data

    def get_podcast_information(self, key: str) -> PodcastInfo:
        """ Return information about podcast. """
        result = PodcastInfo.from_json(
            self.podcast.get(key, None) if self.podcast is not None else None
        )

        result.url_prefix = \
            self.podcast.get('url_prefix', "") if self.podcast is not None else ""

        return result

    def __str__(self) -> str:
        """
        Display settings information.

        @param self: object handle
        @return: formatted configuration
        """
        result = "Youtube configuration:\n"
        result += f"output: {self.output}\n\n"
        for elem in self.sources:
            result += f"  {elem.type}: {elem.type} [{elem.name}]\n"
        return result
