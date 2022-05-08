from argparse import ArgumentParser, Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.factory import FactoryError
from ytrss.core.factory.database import create_database
from ytrss.core.factory.movie import create_movie
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

    def run(self, configuration: YtrssConfiguration, options: Namespace) -> int:
        try:
            movie = create_movie(Url(options.url))
        except FactoryError:
            logger.error("This is not valid url or movie not exists: %s", options.url)
            return 1

        destination = DestinationId(options.destination)
        if destination not in configuration.destination_manager:
            logger.error("Destination [%s] is not defined in configuration", destination)
            return 1

        if create_database(configuration).queue_mp3(movie, destination):
            logger.info("Movie [%s] added to queue", options.url)
        else:
            logger.error("Cannot add this url: %s to queue. It is probably downloaded", options.url)
            return 2
        return 0
