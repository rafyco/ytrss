import re

from ytrss.configuration.entity.source import Source
from ytrss.core.entity.source_downloader import SourceDownloaderError
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube.base_youtube_source_downloader import BaseYouTubeSourceDownloader


class YouTubeChannelSourceDownloader(BaseYouTubeSourceDownloader):
    """ YouTube channel source Downloader

    Implementation of source downloader for channel on YouTube
    """

    def __init__(self, source: Source) -> None:
        match = re.match(r"https?:\/\/(www\.)?youtube\.com\/channel\/(?P<code>[\dA-Za-z_\-]+)", source.url)
        if match is None:
            raise SourceDownloaderError()
        self._code = match.group('code')
        BaseYouTubeSourceDownloader.__init__(self, source)

    @property
    def source_url(self) -> Url:
        return Url(f"https://www.youtube.com/feeds/videos.xml?channel_id={self._code}")
