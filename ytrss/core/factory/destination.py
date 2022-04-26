from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.controlers.rss.destination import RssDestination
from ytrss.core.entity.destination import Destination
from ytrss.core.factory import BaseFactory


class DestinationFactory(BaseFactory[DestinationInfo, Destination]):

    @classmethod
    def build(cls, param: DestinationInfo) -> Destination:
        return RssDestination(param.identity, param)


create_destination = DestinationFactory()
