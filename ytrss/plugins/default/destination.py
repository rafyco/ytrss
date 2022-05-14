import os
import shutil
from typing import Iterator, Sequence

from ytrss.core.entity.destination import Destination, DestinationError

from ytrss.core.entity.downloaded_movie import DownloadedMovie, MovieFileError

from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Path
from ytrss.core.managers.templates_manager import TemplatesManager


class DefaultDestination(Destination):
    """
    A destination copy files to destination folder.
    """

    def __init__(self, info: DestinationInfo) -> None:
        # pylint: disable=C0123
        if type(self) == DefaultDestination and info.type != 'default' and info.type != 'copy':
            raise DestinationError()
        self.__info = info

    @property
    def identity(self) -> DestinationId:
        return self.__info.identity

    @property
    def info(self) -> DestinationInfo:
        return self.__info

    @property
    def saved_movies(self) -> Iterator[DownloadedMovie]:
        if self.info.output_path is None:
            logger.error("output_path is None")
            return
        for filename in os.listdir(self.info.output_path):
            if filename.endswith(".json"):
                try:
                    yield DownloadedMovie.from_file(self.info.output_path, filename)
                except MovieFileError as ex:
                    logger.info(ex)

    def save(self, files: Sequence[Path], templates_manager: TemplatesManager) -> None:
        if self.info.output_path is None:
            raise KeyError
        os.makedirs(self.info.output_path, exist_ok=True)
        for file in files:
            try:
                shutil.move(file, self.info.output_path)
            except shutil.Error as ex:
                logger.error(ex)
        self.on_finish(templates_manager)
