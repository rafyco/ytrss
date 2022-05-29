import os
import shutil
from argparse import Namespace, ArgumentParser

from ytrss.commands import BaseCommand
from ytrss.core.entity.movie import MovieError
from ytrss.core.helpers.exceptions import DownloadMovieError
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
            movie = self.manager_service.plugin_manager.create_movie(Url(options.url))

        except MovieError:
            logger.error("This is not valid url or movie not exists: %s", options.url)
            return 1

        try:
            downloaded_movie = self\
                .manager_service\
                .plugin_manager\
                .download_movie(movie,
                                self.manager_service.configuration)
            self.manager_service.plugin_manager.modify_res_files(downloaded_movie, self.manager_service.configuration)
        except DownloadMovieError:
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
