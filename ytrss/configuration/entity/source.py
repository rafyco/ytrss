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
Module with source data object
"""
from typing import Dict, Any

from ytrss.configuration.consts import DEFAULT_PODCAST_DIR


class Source:
    """
    Source data object

    This object contains an information about source, where the podcast can be downloaded
    """

    def __init__(self) -> None:
        self.code: str = "none"
        self.type: str = "default"
        self.destination_dir: str = DEFAULT_PODCAST_DIR
        self.name: str = "<unknown>"
        self.enable: bool = True

    @property
    def json(self) -> Dict[str, Any]:
        """
        Dictionary representation of file
        """
        return {
            "name": self.name,
            "code": self.code,
            "type": self.type,
            "destination_dir": self.destination_dir,
            "enable": self.enable
        }

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'Source':
        """ Create Source object from dictionary. """
        source = Source()
        if 'name' in json and isinstance(json['name'], str):
            source.name = json['name']
        if 'code' in json and isinstance(json['code'], str):
            source.code = json['code']
        if 'type' in json and isinstance(json['type'], str):
            source.type = json['type']
        if 'destination_dir' in json and isinstance(json['destination_dir'], str):
            source.destination_dir = json['destination_dir']
        if 'enable' in json and isinstance(json['enable'], bool):
            source.enable = json['enable']
        return source
