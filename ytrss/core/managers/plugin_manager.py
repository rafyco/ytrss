from typing import List, Sequence

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.destination import Destination, DestinationError
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.movie import Movie, MovieError
from ytrss.core.entity.plugin import BasePlugin
from ytrss.core.entity.source_downloader import SourceDownloader, SourceDownloaderError
from ytrss.core.helpers.exceptions import DownloadMovieError
from ytrss.core.helpers.typing import Url
from ytrss.plugins.default.plugin import DefaultPlugin
from ytrss.plugins.mp3_tags.plugin import Mp3TagsPlugin
from ytrss.plugins.rss.plugin import RssPlugin
from ytrss.plugins.youtube.plugin import YouTubePlugin
from ytrss.plugins.youtube_dl.plugin import YouTubeDlPlugin


class PluginManager(BasePlugin):
    """ Plugin Manager """

    def __init__(self) -> None:
        self._plugins: List[BasePlugin] = [
            DefaultPlugin(),
            RssPlugin(),
            YouTubePlugin(),
            YouTubeDlPlugin(),
            Mp3TagsPlugin()
        ]

    @property
    def plugins(self) -> Sequence[BasePlugin]:
        """ List of plugins"""
        return self._plugins

    def create_movie(self, url: Url) -> Movie:
        for plugin in self._plugins:
            try:
                movie = plugin.create_movie(url)  # pylint: disable=E1128
                if movie is not None:
                    return movie
            except Exception:  # pylint: disable=W0703
                pass
        raise MovieError()

    def create_destination(self, info: DestinationInfo) -> Destination:
        for plugin in self._plugins:
            try:
                destination = plugin.create_destination(info)
                if destination is not None:
                    return destination
            except Exception:  # pylint: disable=W0703
                pass
        raise DestinationError()

    def download_movie(self, movie: Movie, configuration: YtrssConfiguration) -> DownloadedMovie:
        for plugin in self._plugins:
            try:
                downloaded_movie = plugin.download_movie(movie, configuration)  # pylint: disable=E1128
                if downloaded_movie is not None:
                    return downloaded_movie
            except Exception:  # pylint: disable=W0703
                pass
        raise DownloadMovieError()

    def create_source_downloader(self, source: Source) -> SourceDownloader:
        for plugin in self._plugins:
            try:
                source_downloader = plugin.create_source_downloader(source)  # pylint: disable=E1128
                if source_downloader is not None:
                    return source_downloader
            except Exception:  # pylint: disable=W0703
                pass
        raise SourceDownloaderError()

    def modify_res_files(self, downloaded_movie: DownloadedMovie, configuration: YtrssConfiguration) -> None:
        for plugin in self._plugins:
            # try:
            plugin.modify_res_files(downloaded_movie, configuration)
            # except Exception as ex:  # pylint: disable=W0703
            #     logger.error("Problem with modify file: %s", ex)
