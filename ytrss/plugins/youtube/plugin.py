from typing import Optional, Callable, List

from ytrss.configuration.entity.source import Source
from ytrss.core.entity.plugin import Plugin
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.plugins.youtube.youtube_channel_source_downloader import YouTubeChannelSourceDownloader
from ytrss.plugins.youtube.youtube_named_channel_source_downloader import YouTubeNamedChannelSourceDownloader
from ytrss.plugins.youtube.youtube_playlist_source_downloader import YouTubePlaylistSourceDownloader


class YouTubePlugin(Plugin):
    """ Plugin with sources for YouTube site """

    def create_source_downloader(self, source: Source) -> Optional[SourceDownloader]:
        sources_constructs: List[Callable[[Source], SourceDownloader]] = [
            YouTubePlaylistSourceDownloader,
            YouTubeChannelSourceDownloader,
            YouTubeNamedChannelSourceDownloader
        ]

        for source_downloader_class in sources_constructs:
            try:
                source_downloader = source_downloader_class(source)
                if source_downloader is not None:
                    return source_downloader
            except Exception:  # pylint: disable=W0703
                pass
        return None
