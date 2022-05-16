import os
from typing import Sequence

import youtube_dl

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.downloader import Downloader, DownloaderError
from ytrss.core.entity.movie import Movie

from ytrss.core.helpers.files import cwd
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Path
from ytrss.plugins.youtube_dl.movie import YouTubeMovie


class YouTubeDownloader(Downloader):
    """
    YouTube downloader

    Downloader that use `youtube_dl <https://rg3.github.io/youtube-dl/>`_ implementation. It downloads
    a movie file from any url that can be use by `youtube_dl` service.
    """

    def __init__(self, movie: Movie, configuration: YtrssConfiguration) -> None:
        if not isinstance(movie, YouTubeMovie):
            raise DownloaderError()
        self.configuration = configuration
        self._movie = movie

    @classmethod
    def __invoke_ytdl(cls, args: Sequence[str]) -> int:
        try:
            youtube_dl.main(args)
            status = 0
        except SystemExit as ex:
            if ex.code is None:
                status = 0
            else:
                status = ex.code  # pylint: disable=E0012,R0204
        return status

    def download(self) -> DownloadedMovie:
        try:
            os.makedirs(self.configuration.cache_path)
        except OSError:
            pass

        with cwd(self.configuration.cache_path):

            logger.info("Downloading movie: [%s] %s", self._movie.url, self._movie.title)
            status = self.__invoke_ytdl(list(self.configuration.args) + ['-o', f"{self._movie.identity}.mp3",
                                                                         self._movie.url])

            if status != 0:
                raise DownloaderError(f"youtube_dl raise with state: {status}")

            full_file_name = Path(f"{self._movie.identity}.mp3")
            if not os.path.isfile(full_file_name):
                raise DownloaderError(f"File {full_file_name} not downloaded")

        return DownloadedMovie.create_movie_desc(self.configuration.cache_path, self._movie, [full_file_name])
