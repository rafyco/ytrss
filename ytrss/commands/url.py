from argparse import ArgumentParser, Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import InvalidParameterMovieError
from ytrss.core.factory.database import create_database
from ytrss.core.factory.movie import create_movie
from ytrss.core.logging import logger
from ytrss.core.typing import Url


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

    def run(self, configuration: Configuration, options: Namespace) -> int:
        try:
            movie = create_movie(Url(options.url))
        except InvalidParameterMovieError:
            logger.info("This is not valid url: %s", options.url)
            return 1

        destination = DestinationId(options.destination)
        if destination not in configuration.conf.destination_manager:
            logger.info("Destination [%s] is not defined in configuration", destination)
            return 1

        if create_database(configuration).queue_mp3(movie, destination):
            logger.info("Movie [%s] added to queue", options.url)
        else:
            logger.info("Cannot add this url: %s to queue. It is probably downloaded", options.url)
            return 2
        return 0
