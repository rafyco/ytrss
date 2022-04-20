"""
Finding YouTube movie urls.
"""

import logging
from typing import Optional, Union, List, Sequence, Iterator

from ytrss.configuration.entity.source import Source
from ytrss.core.factory import CoreFactoryError
from ytrss.core.factory.source_downloader import create_source_downloader
from ytrss.database.entity.movie_task import MovieTask
from ytrss.download.source_downloader import SourceDownloader


class URLFinder:
    """
    Finding YouTube movie urls from configuration.

    @ivar __sources: table with source's urls
    @type __sources: list
    """
    def __init__(self, sources: Optional[Sequence[Source]] = None) -> None:
        """
        URLFinder constructor.
        """
        self.__sources: List[SourceDownloader] = []
        if sources is not None:
            self.__add_source(sources)

    def __add_source(self, source: Union[Source, Sequence[Source]]) -> None:
        """
        Add subscription code url.

        @param self: handle object
        @type self: L{URLFinder}
        @param source: subscription's code
        @type source: str
        """
        if isinstance(source, Source):
            logging.debug("add user source: %s, [type: %s]", source.name, source.type)
            try:
                self.__sources.append(create_source_downloader(source))
            except CoreFactoryError:
                pass
        else:
            for elem in source:
                self.__add_source(elem)

    @property
    def movies(self) -> Iterator[MovieTask]:
        """
        Get urls to YouTube movies.

        @param self: handle object
        @type self: L{URLFinder}
        @return: List of elements to download
        @rtype: L{Element<ytrss.core.element.Element>}
        """
        for source in self.__sources:
            logging.debug("Container: %s", source)
            for movie_task in source.movies:
                logging.debug("El: %s", movie_task.movie)
                yield movie_task
