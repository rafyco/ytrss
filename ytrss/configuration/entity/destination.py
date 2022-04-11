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
"""
Module with destination information
"""
from ytrss.configuration.consts import DEFAULT_PODCAST_DIR
from ytrss.core.typing import Path


class Destination:
    """
    Destination information object
    """

    def __init__(self) -> None:
        self.destination_dir: Path = Path(DEFAULT_PODCAST_DIR)

    @staticmethod
    def from_json(json: str) -> 'Destination':
        """
        Create podcast information object from dictionary
        """
        destination = Destination()
        destination.destination_dir = Path(json)
        return destination

    @property
    def identity(self) -> str:
        """ Destination id """
        return self.destination_dir
