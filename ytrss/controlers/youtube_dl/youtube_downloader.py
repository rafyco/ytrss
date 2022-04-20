"""
Download mp3 file from YouTube using I{youtube_dl} library.

@see: U{https://rg3.github.io/youtube-dl/}
"""

import os
import json
import logging
from typing import Sequence

import youtube_dl

from ytrss.core.entity.downloader import Downloader, DownloaderError
from ytrss.core.entity.movie import Movie

from ytrss.configuration.configuration import Configuration
from ytrss.core.typing import Path


class YouTubeDownloader(Downloader):
    """
    Download mp3 file from YouTube.

    Class download file to cache folder. In case of success files are
    moved to output file. Output and cache folder are describe in
    L{YTSettings<ytrss.core.settings.YTSettings>} object.

    """
    def __init__(self, configuration: Configuration) -> None:
        """
        Downloader constructor.
        """
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
        """
        Download YouTube movie.

        Function download movie, convert to mp3 and move to output file.
        """
        try:
            os.makedirs(self.configuration.conf.cache_path)
        except OSError:
            pass
        current_path = os.getcwd()
        os.chdir(self.configuration.conf.cache_path)

        logging.info("url: %s", movie.url)
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
            file_handler.write(json.dumps(movie.json))

        os.chdir(current_path)

        return [source_path, metadata_path]
