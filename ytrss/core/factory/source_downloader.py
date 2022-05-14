from typing import Callable, Optional, Sequence

from ytrss.configuration.entity.source import Source
from ytrss.core.factory import BaseFactory
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.plugins.youtube.youtube_channel_source_downloader import YouTubeChannelSourceDownloader
from ytrss.plugins.youtube.youtube_named_channel_source_downloader import \
    YouTubeNamedChannelSourceDownloader
from ytrss.plugins.youtube.youtube_playlist_source_downloader import YouTubePlaylistSourceDownloader


class SourceDownloaderFactory(BaseFactory[Source, SourceDownloader]):
    """
    Factory for SourceDownloader object
    """

    @property
    def plugins(self) -> Sequence[Callable[[Source], Optional[SourceDownloader]]]:
        """ A list of functions that try to produce an object """
        return [
            YouTubeChannelSourceDownloader,
            YouTubeNamedChannelSourceDownloader,
            YouTubePlaylistSourceDownloader
        ]


create_source_downloader = SourceDownloaderFactory()
