import os
import shutil
from argparse import Namespace, ArgumentParser

from ytrss.core.entity.downloader import DownloaderError
from ytrss.core.factory import FactoryError
from ytrss.core.factory.downloader import create_downloader

from ytrss.core.factory.movie import create_movie

from ytrss.commands import BaseCommand
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Url


class DownloadCommand(BaseCommand):
    """
    Immediately download a movie to current location.
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "download")

    def arg_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("url",
                            help="Url that should be downloaded")

    def run(self, options: Namespace) -> int:
        try:
            movie = create_movie(Url(options.url))

        except FactoryError:
            logger.error("This is not valid url or movie not exists: %s", options.url)
            return 1

        try:
            downloader = create_downloader(self.manager_service.configuration)
            downloaded_movie = downloader.download(movie)
        except FactoryError:
            logger.error("Downloader create problem")
            return 1
        except DownloaderError:
            logger.error("There are no downloaded files for movie from: %s", movie.url)
            return 1

        destination_path = os.path.join(os.getcwd(), movie.identity)
        os.makedirs(destination_path, exist_ok=True)
        for file in downloaded_movie.data_paths:
            try:
                shutil.move(file, destination_path)
            except shutil.Error as ex:
                logger.error(ex)
        return 0
