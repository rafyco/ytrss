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
