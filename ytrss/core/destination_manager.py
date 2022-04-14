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
from typing import Dict, Iterator

from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.core.entity.destination import Destination
from ytrss.core.factory.destination import create_destination


class DestinationManager:
    """
    Destination manager

    An object that managed all destinations available in application.
    """

    def __init__(self) -> None:
        self._destinations: Dict[DestinationId, Destination] = {}

    def add_from_info(self, info: DestinationInfo) -> None:
        """
        Add a destination from DestinationInfo object.
        """
        self._destinations[info.identity] = create_destination(info)

    def __getitem__(self, key: DestinationId) -> Destination:
        if key in self._destinations:
            return self._destinations[key]
        raise KeyError  # TODO: Default destination from code

    @property
    def destinations(self) -> Iterator[Destination]:
        """
        Creator of all destinations available from manager.
        """
        for key in self._destinations:
            yield self._destinations[key]
