from typing import List, Iterable
from urllib.request import urlopen
from xml.dom import minidom

from ytrss.configuration.entity.source import Source
from ytrss.controlers.youtube_dl.movie import YouTubeMovie
from ytrss.core.logging import logger
from ytrss.core.typing import Url
from ytrss.database.entity.movie_task import MovieTask
from ytrss.download.source_downloader import SourceDownloader


class YouTubeSourceDownloader(SourceDownloader):

    def __init__(self, source: Source) -> None:
        self.url = source.url
        self.destination = source.destination
        self.link_type = source.type
        if self.link_type != "user" and self.link_type != "playlist" and self.link_type != "default":
            raise AttributeError("link_type must be 'user' or 'playlist'")

    @property
    def _source_url(self) -> Url:
        pattern = "channel_id"
        if self.link_type == 'playlist':
            pattern = "playlist_id"
        return Url(f"https://www.youtube.com/feeds/videos.xml?{pattern}={self.url}")

    @property
    def movies(self) -> Iterable[MovieTask]:
        logger.debug("URL: %s", self._source_url)

        result: List[MovieTask] = []
        try:
            xml_str = urlopen(self._source_url).read()
            xmldoc = minidom.parseString(xml_str)
            tags = xmldoc.getElementsByTagName('link')
        # We want catch every exception in ulr like invalid channel or web
        except Exception:  # pylint: disable=W0703
            logger.error("Problem with url: %s", self._source_url)
            return result
        for elem in tags:
            url: Url = Url(elem.getAttribute("href"))
            if "watch?v=" in url:  # pylint: disable=E1135
                yield MovieTask.from_objects(YouTubeMovie(url), self.destination)
        return result
