from typing import List, Iterator, Tuple

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.movie import Movie
from ytrss.core.factory.source_downloader import create_source_downloader
from ytrss.core.entity.source_downloader import SourceDownloader, SourceDownloaderError
from ytrss.core.helpers.logging import logger


class SourcesManager:
    """
    Sources manager

    An object that managed all sources.
    """
    def __init__(self) -> None:
        self._sources: List[SourceDownloader] = []

    def add_from_info(self, source: Source) -> None:
        """ Add source from info file. """
        try:
            self._sources.append(create_source_downloader(source))
        except SourceDownloaderError:
            logger.error("Unknown url: %s", source.url)

    @property
    def movies(self) -> Iterator[Tuple[Movie, DestinationId]]:
        """ List new movies from all registered sources. """
        for source in self._sources:
            for movie, destination in source.movies:
                yield movie, destination
