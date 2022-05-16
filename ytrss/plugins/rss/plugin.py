from typing import Optional

from ytrss.core.entity.destination import Destination

from ytrss.configuration.entity.destination_info import DestinationInfo

from ytrss.core.entity.plugin import Plugin
from ytrss.plugins.rss.destination import RssDestination


class RssPlugin(Plugin):
    """ Plugin with destination that creates rss channel. """

    def create_destination(self, info: DestinationInfo) -> Optional[Destination]:
        return RssDestination(info)
