import os

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.movie import Movie
from ytrss.core.helpers.exceptions import CookieError, DownloadMovieError

from ytrss.core.helpers.files import cwd
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Path
from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.plugins.youtube_dl.wrapper import youtube_main_wrapper, YtDlsArguments


def _download_error(status: int, stderr: str) -> DownloadMovieError:
    """ Create an error from yt_dlp output, without its WARNING lines """
    errors = [line.strip() for line in stderr.splitlines() if line.startswith("ERROR:")]
    message = "\n".join(errors) or f"yt_dlp raise with state: {status}"
    if "--cookies" in message or "cookies are no longer valid" in stderr:
        return CookieError(message)
    return DownloadMovieError(message)


class YouTubeDownloader:
    """
    YouTube downloader

    Downloader that use `yt_dlp <https://rg3.github.io/youtube-dl/>`_ implementation. It downloads
    a movie file from any url that can be use by `yt_dlp` service.
    """

    def __init__(self, movie: Movie, configuration: YtrssConfiguration) -> None:
        if not isinstance(movie, YouTubeMovie):
            raise DownloadMovieError("YouTubeMovie instance not exists")
        self.configuration = configuration
        self._movie = movie

    def download(self) -> DownloadedMovie:
        """ Download movie using YouTube_dl tool """
        try:
            os.makedirs(self.configuration.cache_path)
        except OSError:
            pass

        with cwd(self.configuration.cache_path):
            logger.info("Downloading movie: [%s] %s", self._movie.url, self._movie.title)
            status, _, stderr = youtube_main_wrapper(
                *YtDlsArguments(self.configuration).download_args,
                '-o',
                self._movie.identity,
                self._movie.url,
                show_output=True
            )

            if status != 0:
                raise _download_error(status, stderr)

            for extension in ['mp3', 'mp4', 'webm', 'mkv', 'ogg']:
                full_file_name = Path(f"{self._movie.identity}.{extension}")
                if os.path.isfile(full_file_name):
                    return DownloadedMovie.create_movie_desc(self.configuration.cache_path, self._movie,
                                                             [full_file_name])
        raise DownloadMovieError(f"File {self._movie.identity} not downloaded")
