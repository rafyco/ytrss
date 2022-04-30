import io
import os
import shutil
from typing import Iterator, Sequence

from ytrss.core.entity.destination import Destination
from ytrss.core.factory import CoreFactoryError

from ytrss.plugins.rss.podcast.podcast import Podcast
from ytrss.core.entity.downloaded_movie import DownloadedMovie, MovieFileError

from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Path


class RssDestination(Destination):
    """
    A destination that create Rss feed.
    """

    def __init__(self, destination_id: DestinationId, info: DestinationInfo) -> None:
        self.__identity = destination_id
        self.__info = info

    @property
    def identity(self) -> DestinationId:
        return self.__identity

    @property
    def info(self) -> DestinationInfo:
        return self.__info

    @property
    def dir_path(self) -> Path:
        return Path(self.identity)

    @property
    def saved_movies(self) -> Iterator[DownloadedMovie]:
        if self.info.output_path is None:
            logger.error("output_path is None")
            return
        for filename in os.listdir(self.info.output_path):
            if filename.endswith(".json"):
                try:
                    yield DownloadedMovie(self.info.output_path, filename[0:len(filename) - 5])
                except (MovieFileError, CoreFactoryError) as ex:
                    logger.info(ex)

    def on_finish(self) -> None:
        if self.info.output_path is None:
            raise KeyError
        if os.path.isdir(self.info.output_path):
            logger.info("Generate RSS: %s", self.info.title)
            podcast = Podcast(self.info)
            for movie in self.saved_movies:
                logger.debug(" > %s", movie.title)
                try:
                    podcast.add_item(movie=movie)
                except ValueError:
                    logger.info("Cannot add item to rss [%s] %s", movie.identity, movie.title)
            podcast_file = os.path.join(self.info.output_path, "podcast.xml")
            logger.debug("Create rss file: \"%s\"", podcast_file)
            file_handler = io.open(podcast_file, "w", encoding="utf-8")
            file_handler.write(podcast.generate())
            file_handler.close()

    def save(self, files: Sequence[Path]) -> None:
        if self.info.output_path is None:
            raise KeyError
        os.makedirs(self.info.output_path, exist_ok=True)
        for file in files:
            try:
                shutil.move(file, self.info.output_path)
            except shutil.Error as ex:
                logger.error(ex)
        self.on_finish()
