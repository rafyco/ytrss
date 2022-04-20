"""
Module with download queue object.
"""

import logging
from typing import Optional

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie
from ytrss.database.entity.movie_task import MovieTask
from ytrss.database.file_db.database_file_config import DatabaseFileConfig
from ytrss.database.database_put import DatabasePut
from ytrss.database.file_db.database_file_controller import DatabaseFileController


class FileDatabasePut(DatabasePut):
    """
    Class saving urls to download.

    @ivar url_rss: path to file with readed urls
    @type url_rss: str
    @ivar download_file: file ready to download
    @type download_file: str
    @ivar rememberer: object remembering urls
    @type rememberer: L{DatabaseFileController}
    """

    def __init__(self, configuration: Configuration, base_file: Optional[str] = None):
        """
        DownloadQueue constructor.
        """
        config_file = DatabaseFileConfig(configuration)
        self.url_rss = config_file.url_rss
        self.download_file = config_file.download_file
        self.download_yt = DatabaseFileController(self.download_file)
        base_file = base_file if base_file is not None else config_file.url_rss
        logging.debug(base_file)
        self.rememberer = DatabaseFileController(base_file)

    def queue_mp3(self, movie: Movie, destination: DestinationId) -> bool:
        """
        Add address to download.
        """
        logging.debug("DOWNLOAD: %s", movie.url)
        if self.rememberer.is_new(MovieTask.from_objects(movie, destination)):
            logging.debug("Download address: %s", movie.url)
            self.download_yt.add_movie(MovieTask.from_objects(movie, destination))
            self.rememberer.add_movie(MovieTask.from_objects(movie, destination))
            return True
        return False
