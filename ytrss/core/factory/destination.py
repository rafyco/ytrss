from typing import Optional, Callable, Sequence

from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.plugins.default.destination import DefaultDestination
from ytrss.plugins.rss.destination import RssDestination
from ytrss.core.entity.destination import Destination
from ytrss.core.factory import BaseFactory


class DestinationFactory(BaseFactory[DestinationInfo, Destination]):
    """
    Factory for Destination object
    """

    @property
    def plugins(self) -> Sequence[Callable[[DestinationInfo], Optional[Destination]]]:
        """ A list of functions that try to produce an object """
        return [
            DefaultDestination,
            RssDestination
        ]


create_destination = DestinationFactory()
