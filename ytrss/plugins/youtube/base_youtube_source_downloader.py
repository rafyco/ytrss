from abc import abstractmethod

from typing import Iterable, Tuple, List
from urllib.request import urlopen
from xml.dom import minidom

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube_dl.movie import YouTubeMovie


class BaseYouTubeSourceDownloader(SourceDownloader):

    def __init__(self, source):
        self.url = source.url
        self.destination = source.destination

    @abstractmethod
    def source_url(self) -> Url:
        pass

    @property
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        logger.debug("URL: %s", self.url)

        result: List[Tuple[Movie, DestinationId]] = []
        try:
            xml_str = urlopen(str(self.source_url)).read()
            xmldoc = minidom.parseString(xml_str)
            tags = xmldoc.getElementsByTagName('link')
        # We want catch every exception in ulr like invalid channel or web
        except Exception:  # pylint: disable=W0703
            logger.error("Problem with url: %s", self.url)
            return result
        for elem in tags:
            url: Url = Url(elem.getAttribute("href"))
            if "watch?v=" in url:  # pylint: disable=E1135
                yield YouTubeMovie(url), self.destination
        return result