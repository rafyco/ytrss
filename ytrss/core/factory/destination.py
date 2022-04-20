from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.controlers.rss.destination import RssDestination
from ytrss.core.entity.destination import Destination


def create_destination(info: DestinationInfo) -> Destination:
    """
    Factory of destination object
    """
    return RssDestination(info.identity, info)
