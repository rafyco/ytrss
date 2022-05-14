import re

from ytrss.configuration.entity.source import Source
from ytrss.core.entity.source_downloader import SourceDownloaderError
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube.base_youtube_source_downloader import BaseYouTubeSourceDownloader


class YouTubeNamedChannelSourceDownloader(BaseYouTubeSourceDownloader):
    """ YouTube named channel source Downloader

    Implementation of source downloader for channel on YouTube, where the name is defined in url.
    """

    def __init__(self, source: Source) -> None:
        match = re.match(r"https?:\/\/(www\.)?youtube\.com\/c\/(?P<user>[\dA-Za-z_\-]+)", source.url)
        if match is None:
            raise SourceDownloaderError()
        self._name = match.group('user')
        BaseYouTubeSourceDownloader.__init__(self, source)

    @property
    def source_url(self) -> Url:
        return Url(f"https://www.youtube.com/feeds/videos.xml?user={self._name}")
