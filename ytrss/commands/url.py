from argparse import ArgumentParser, Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import InvalidParameterMovieError
from ytrss.core.factory.database import create_database
from ytrss.core.factory.movie import create_movie
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
            print(f"This is not valid url: {options.url}")
            return 1

        destination = DestinationId(options.destination)
        if destination not in configuration.conf.destination_manager:
            print(f"Destination [{destination}] is not defined in configuration")
            return 1

        if create_database(configuration).queue_mp3(movie, destination):
            print(f"Movie [{options.url}] added to queue")
        else:
            print(f"Cannot add this url: {options.url} to queue. It is probably downloaded")
            return 2
        return 0
