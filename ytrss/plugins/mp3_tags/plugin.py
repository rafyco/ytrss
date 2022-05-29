import os
from urllib.parse import urlparse

from mutagen import File as FileMutagen

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.plugin import Plugin
from ytrss.core.helpers.logging import logger


class Mp3TagsPlugin(Plugin):
    """ Mp3 tags plugin

    Plugin to add metadata to audio files.
    """

    def modify_res_files(self, downloaded_movie: DownloadedMovie, configuration: YtrssConfiguration) -> None:
        for res_file in downloaded_movie.resources_files:
            movie_tags = FileMutagen(os.path.join(configuration.cache_path, res_file), easy=True)

            if movie_tags is None:
                continue

            try:
                movie_tags["title"] = downloaded_movie.title
            except KeyError as key_error:
                logger.warning(key_error)

            try:
                movie_tags["artist"] = downloaded_movie.author
            except KeyError as key_error:
                logger.warning(key_error)

            try:
                movie_tags["album"] = urlparse(downloaded_movie.url).netloc
            except KeyError as key_error:
                logger.warning(key_error)

            try:
                movie_tags["comment"] = downloaded_movie.description
            except KeyError as key_error:
                logger.warning(key_error)

            try:
                movie_tags["date"] = downloaded_movie.date.strftime("%Y-%m-%d")
            except KeyError as key_error:
                logger.warning(key_error)

            movie_tags.save()
