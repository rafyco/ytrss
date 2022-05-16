from argparse import ArgumentParser, Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import MovieError
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Url


class UrlCommand(BaseCommand):
    """
    Add url to download
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "url")

    def arg_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("url",
                            help="Url that should be downloaded")
        parser.add_argument("-d", "--destination", dest="destination",
                            help="destination [default: default]", default="default", metavar="DEST")

    def run(self, options: Namespace) -> int:
        try:
            movie = self.manager_service.plugin_manager.create_movie(Url(options.url))
        except MovieError:
            logger.error("This is not valid url or movie not exists: %s", options.url)
            return 1

        destination = DestinationId(options.destination)
        if destination not in self.manager_service.destination_manager:
            logger.error("Destination [%s] is not defined in configuration", destination)
            return 1

        if self.manager_service.database.queue_mp3(movie, destination):
            logger.info("Movie [%s] added to queue", options.url)
        else:
            logger.error("Cannot add this url: %s to queue. It is probably downloaded", options.url)
            return 2
        return 0
