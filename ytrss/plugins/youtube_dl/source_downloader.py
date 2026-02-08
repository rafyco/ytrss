from typing import Iterable, Tuple

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.movie import Movie
from ytrss.core.entity.source_downloader import SourceDownloader, SourceDownloaderError
from ytrss.core.helpers.typing import Url
from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.plugins.youtube_dl.wrapper import youtube_main_wrapper


class YouTubeDlSourceDownloader(SourceDownloader):
    """ YouTube Source Downloader

    This object put a list of movies from source if its support by `yt-dlp`
    """

    def __init__(self, source: Source) -> None:
        self.url = source.url
        self.destination = source.destination
        status, output, error = youtube_main_wrapper(
            '--flat-playlist',
            '--playlist-end',
            '20', '--print',
            'url',
            self.url
        )
        self.output = output
        if status != 0:
            raise SourceDownloaderError(f'Invalid url source (self.url): {error}')

    @property
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        for url in self.output.splitlines():
            try:
                yield YouTubeMovie(Url(url)), self.destination
            except Exception:  # pylint: disable=W0703
                pass
