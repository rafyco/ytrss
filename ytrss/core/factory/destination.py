from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.controlers.rss.destination import RssDestination
from ytrss.core.entity.destination import Destination
from ytrss.core.factory import BaseFactory


class DestinationFactory(BaseFactory[DestinationInfo, Destination]):
    """
    Factory for Destinations
    """

    @classmethod
    def build(cls, param: DestinationInfo) -> Destination:
        """
        Build defined object from parameter
        """
        return RssDestination(param.identity, param)


create_destination = DestinationFactory()
