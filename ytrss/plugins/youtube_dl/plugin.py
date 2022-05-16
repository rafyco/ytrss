from typing import Optional

from ytrss.core.entity.downloader import Downloader

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.entity.movie import Movie, MovieError
from ytrss.core.entity.plugin import Plugin
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.plugins.youtube_dl.youtube_downloader import YouTubeDownloader


class YouTubeDlPlugin(Plugin):
    """ Plugin implements mechanisms from youtube_dl """

    def create_movie(self, url: Url) -> Optional[Movie]:
        try:
            return YouTubeMovie(url)
        except MovieError:
            return None

    def create_downloader(self, movie: Movie, configuration: YtrssConfiguration) -> Optional[Downloader]:
        return YouTubeDownloader(movie, configuration)
