from typing import Optional, Union, List, Sequence, Iterator

from ytrss.configuration.entity.source import Source
from ytrss.core.factory import CoreFactoryError
from ytrss.core.factory.source_downloader import create_source_downloader
from ytrss.database.entity.movie_task import MovieTask
from ytrss.download.source_downloader import SourceDownloader


class URLFinder:
    def __init__(self, sources: Optional[Sequence[Source]] = None) -> None:
        self.__sources: List[SourceDownloader] = []
        if sources is not None:
            self.__add_source(sources)

    def __add_source(self, source: Union[Source, Sequence[Source]]) -> None:
        if isinstance(source, Source):
            try:
                self.__sources.append(create_source_downloader(source))
            except CoreFactoryError:
                pass
        else:
            for elem in source:
                self.__add_source(elem)

    @property
    def movies(self) -> Iterator[MovieTask]:
        for source in self.__sources:
            for movie_task in source.movies:
                yield movie_task
