from typing import Optional

from ytrss.configuration.entity.source import Source
from ytrss.core.entity.downloaded_movie import DownloadedMovie

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.entity.movie import Movie, MovieError
from ytrss.core.entity.plugin import Plugin
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.plugins.youtube_dl.source_downloader import YouTubeDlSourceDownloader
from ytrss.plugins.youtube_dl.youtube_downloader import YouTubeDownloader


class YouTubeDlPlugin(Plugin):
    """ Plugin implements mechanisms from yt_dlp """

    def __init__(self, configuration: YtrssConfiguration):
        self._configuration = configuration

    def create_movie(self, url: Url) -> Optional[Movie]:
        try:
            return YouTubeMovie(url, self._configuration)
        except MovieError:
            return None

    def download_movie(self, movie: Movie) -> Optional[DownloadedMovie]:
        return YouTubeDownloader(movie, self._configuration).download()

    def create_source_downloader(self, source: Source) -> Optional[SourceDownloader]:
        return YouTubeDlSourceDownloader(source, self._configuration)
