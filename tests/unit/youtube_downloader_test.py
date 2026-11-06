"""
Tests of YouTube downloader.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from ytrss.core.helpers.exceptions import CacheError, DownloadMovieError
from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.plugins.youtube_dl.youtube_downloader import YouTubeDownloader

WRAPPER = "ytrss.plugins.youtube_dl.youtube_downloader.youtube_main_wrapper"


class TestYouTubeDownloader(unittest.TestCase):
    """
    Tests of YouTubeDownloader.download
    """

    def setUp(self) -> None:
        self.addCleanup(os.chdir, os.getcwd())
        cache = tempfile.TemporaryDirectory()  # pylint: disable=R1732
        self.addCleanup(cache.cleanup)
        self.configuration = MagicMock()
        self.configuration.cache_path = cache.name
        self.configuration.database_path = cache.name
        self.configuration.args = []
        self.movie = MagicMock(spec=YouTubeMovie)
        self.movie.identity = "ytdl:youtube:abc"
        self.movie.url = "https://example.com/watch?v=abc"
        self.movie.title = "title"

    def test_keeps_error_lines_only(self) -> None:
        """ The message has ERROR lines from stderr, without WARNING lines """
        stderr = "WARNING: slow connection\nERROR: [youtube] abc: Video unavailable\n"
        with patch(WRAPPER, return_value=(1, "", stderr)):
            with self.assertRaises(CacheError) as context:
                YouTubeDownloader(self.movie, self.configuration).download()

        self.assertEqual(str(context.exception), "ERROR: [youtube] abc: Video unavailable")

    def test_status_when_no_error_lines(self) -> None:
        """ The message has a status when stderr has no ERROR line """
        with patch(WRAPPER, return_value=(2, "", "WARNING: slow connection\n")):
            with self.assertRaisesRegex(CacheError, "^yt_dlp raise with state: 2$"):
                YouTubeDownloader(self.movie, self.configuration).download()

    def test_file_not_downloaded(self) -> None:
        """ A missing file is a CacheError """
        with patch(WRAPPER, return_value=(0, "", "")):
            with self.assertRaisesRegex(CacheError, "File ytdl:youtube:abc not downloaded"):
                YouTubeDownloader(self.movie, self.configuration).download()

    def test_other_movie_type_is_not_cache_error(self) -> None:
        """ A movie for another plugin stays plain DownloadMovieError """
        with self.assertRaises(DownloadMovieError) as context:
            YouTubeDownloader(MagicMock(), self.configuration)

        self.assertNotIsInstance(context.exception, CacheError)


if __name__ == "__main__":
    unittest.main()
