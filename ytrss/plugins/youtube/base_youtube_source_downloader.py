from abc import abstractmethod

from typing import Iterable, Tuple
from urllib.request import urlopen
from xml.dom import minidom

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.movie import Movie
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube_dl.movie import YouTubeMovie


class BaseYouTubeSourceDownloader(SourceDownloader):
    """ Base YouTube source downloader

    Object that implements source downloader that look for movie from YouTube.
    """

    def __init__(self, source: Source) -> None:
        self.url = source.url
        self.destination = source.destination

    @property
    @abstractmethod
    def source_url(self) -> Url:
        """ Rss url with movies on YouTube """

    @property
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        logger.debug("Source url: %s", self.url)

        try:
            with urlopen(str(self.source_url)) as xml_str:
                xmldoc = minidom.parseString(xml_str.read())
                tags = xmldoc.getElementsByTagName('link')
        # We want catch every exception in ulr like invalid channel or web
        except Exception:  # pylint: disable=W0703
            logger.error("Problem with url: %s", self.url)
            return
        for elem in tags:
            url: Url = Url(elem.getAttribute("href"))
            if "watch?v=" in url:  # pylint: disable=E1135
                try:
                    yield YouTubeMovie(url), self.destination
                except Exception:  # pylint: disable=W0703
                    logger.error("Problem with url in source: %s", self.url)
