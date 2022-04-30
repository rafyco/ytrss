from typing import Callable, Optional, Sequence

from ytrss.configuration.entity.source import Source
from ytrss.core.factory import BaseFactory
from ytrss.core.entity.source_downloader import SourceDownloader, SourceDownloaderError
from ytrss.plugins.youtube.youtube_channel_source_downloader import YouTubeChannelSourceDownloader
from ytrss.plugins.youtube.youtube_named_channel_source_downloader import \
    YouTubeNamedChannelSourceDownloader
from ytrss.plugins.youtube.youtube_playlist_source_downloader import YouTubePlaylistSourceDownloader


class SourceDownloaderFactory(BaseFactory[Source, SourceDownloader]):

    @classmethod
    def build(cls, param: Source) -> SourceDownloader:

        sources: Sequence[Callable[[Source], Optional[SourceDownloader]]] = [
            YouTubeChannelSourceDownloader,
            YouTubeNamedChannelSourceDownloader,
            YouTubePlaylistSourceDownloader
        ]

        for source in sources:
            try:
                result = source(param)
                if result is not None:
                    return result
            except SourceDownloaderError:
                pass
        raise SourceDownloaderError()


create_source_downloader = SourceDownloaderFactory()
