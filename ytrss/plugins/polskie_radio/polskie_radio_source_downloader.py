from typing import Iterable, Tuple
import re
from urllib.request import urlopen
from xml.dom import minidom

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.movie import Movie
from ytrss.core.entity.source_downloader import SourceDownloader, SourceDownloaderError
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Url
from ytrss.plugins.polskie_radio.movie import PolskieRadioMovie


class PolskieRadioSourceDownloader(SourceDownloader):

    def __init__(self, source: Source) -> None:
        match = re.match(r"https?:\/\/(www\.)?polskieradio\.pl\/(?P<name>[A-Za-z\d,]*)/(?P<identity>\d+)", source.url)
        if match is None:
            raise SourceDownloaderError()
        self._id = match.group('identity')
        self._name = match.group('name')
        self.url = source.url
        self.destination = source.destination

    @property
    def source_url(self) -> Url:
        return Url(f"https://www.polskieradio.pl/{self._name}/{self._id}")

    @property
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        logger.error("RAF >>>>> source url checks: %s", self.url)
        try:
            xml_str = urlopen(str(self.source_url)).read()
            xmldoc = minidom.parseString(xml_str)
            tags = xmldoc.getElementsByTagName('link')
        # We want catch every exception in ulr like invalid channel or web
        except Exception:  # pylint: disable=W0703
            logger.error("Problem with url: %s", self.url)
            return
        for elem in tags:
            url: Url = Url(elem.getAttribute("href"))
            if "watch?v=" in url:  # pylint: disable=E1135
                try:
                    yield PolskieRadioMovie(url), self.destination
                except Exception:  # pylint: disable=W0703
                    logger.error("Problem with url in source: %s", self.url)
        return []
