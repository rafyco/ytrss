import os
import json
from typing import Sequence

import youtube_dl

from ytrss.core.entity.downloader import Downloader, DownloaderError
from ytrss.core.entity.movie import Movie

from ytrss.configuration.configuration import Configuration
from ytrss.core.helpers.files import cwd
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Path


class YouTubeDownloader(Downloader):
    """
    YouTube downloader

    Downloader that use `youtube_dl <https://rg3.github.io/youtube-dl/>`_ implementation. It downloads
    a movie file from any url that can be use by `youtube_dl` service.
    """

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

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

    def download(
            self,
            movie: Movie
    ) -> Sequence[Path]:
        try:
            os.makedirs(self.configuration.conf.cache_path)
        except OSError:
            pass

        with cwd(self.configuration.conf.cache_path):

            logger.info("Downloading movie: [%s] %s", movie.url, movie.title)
            status = self.__invoke_ytdl(self.configuration.conf.args + ['-o', f"{movie.identity}.mp3", movie.url])

            if status != 0:
                raise DownloaderError(f"youtube_dl raise with state: {status}")

            full_file_name = f"{movie.identity}.mp3"
            metadata_name = f"{movie.identity}.json"
            if not os.path.isfile(full_file_name):
                raise DownloaderError(f"File {full_file_name} not downloaded")

            source_path = Path(os.path.join(self.configuration.conf.cache_path, full_file_name))
            metadata_path = Path(os.path.join(self.configuration.conf.cache_path, metadata_name))

            with open(metadata_path, 'w') as file_handler:
                file_handler.write(json.dumps(movie.json, indent=4, sort_keys=True))

        return [source_path, metadata_path]
