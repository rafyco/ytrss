from typing import Optional

from ytrss.core.entity.destination import Destination

from ytrss.configuration.entity.destination_info import DestinationInfo

from ytrss.core.entity.plugin import Plugin
from ytrss.plugins.default.destination import DefaultDestination


class DefaultPlugin(Plugin):
    """ Plugin with default destination.

    All movies send to this destination will be only saved to selected directory.
    """

    def create_destination(self, info: DestinationInfo) -> Optional[Destination]:
        return DefaultDestination(info)
