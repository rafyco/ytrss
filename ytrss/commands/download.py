import os
import shutil
from argparse import Namespace, ArgumentParser

from ytrss.core.factory.downloader import create_downloader

from ytrss.core.entity.movie import InvalidParameterMovieError
from ytrss.core.factory.movie import create_movie

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.core.logging import logger
from ytrss.core.typing import Url


class DownloadCommand(BaseCommand):
    """
    Immediately download a movie to current location.
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "download")

    def arg_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("url",
                            help="Url that should be downloaded")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        try:
            movie = create_movie(Url(options.url))
        except InvalidParameterMovieError:
            logger.error("This is not valid url: %s", options.url)
            return 1

        downloader = create_downloader(configuration)

        files = downloader.download(movie)

        if len(list(files)) <= 1:
            logger.error("There are no downloaded files for movie from: %s", movie.url)

        destination_path = os.path.join(os.getcwd(), movie.identity)
        os.makedirs(destination_path, exist_ok=True)
        for file in files:
            try:
                shutil.move(file, destination_path)
            except shutil.Error as ex:
                logger.error(ex)
