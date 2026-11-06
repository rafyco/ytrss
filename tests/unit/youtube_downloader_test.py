"""
Tests of YouTube downloader.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from ytrss.core.helpers.exceptions import CookieError, DownloadMovieError
from ytrss.plugins.youtube_dl.movie import YouTubeMovie
from ytrss.plugins.youtube_dl.plugin import YouTubeDlPlugin
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

    def download_error(self, status: int, stderr: str) -> DownloadMovieError:
        """ Run download with given yt_dlp output and return the raised error """
        with patch(WRAPPER, return_value=(status, "", stderr)):
            with self.assertRaises(DownloadMovieError) as context:
                YouTubeDownloader(self.movie, self.configuration).download()
        return context.exception

    def test_keeps_error_lines_only(self) -> None:
        """ The message has ERROR lines from stderr, without WARNING lines """
        error = self.download_error(1, "WARNING: slow connection\nERROR: [youtube] abc: Video unavailable\n")

        self.assertEqual(str(error), "ERROR: [youtube] abc: Video unavailable")
        self.assertNotIsInstance(error, CookieError)

    def test_status_when_no_error_lines(self) -> None:
        """ The message has a status when stderr has no ERROR line """
        error = self.download_error(2, "WARNING: slow connection\n")

        self.assertEqual(str(error), "yt_dlp raise with state: 2")
        self.assertNotIsInstance(error, CookieError)

    def test_login_required_is_cookie_error(self) -> None:
        """ yt_dlp asks for cookies when it cannot connect without a valid login """
        message = "ERROR: [youtube] abc: Sign in to confirm you're not a bot. Use --cookies for the authentication."
        error = self.download_error(1, f"{message}\n")

        self.assertIsInstance(error, CookieError)
        self.assertEqual(str(error), message)

    def test_rotated_cookies_is_cookie_error(self) -> None:
        """ yt_dlp warns about cookies that are not valid anymore """
        error = self.download_error(
            1,
            "WARNING: [youtube] The provided YouTube account cookies are no longer valid.\n"
            "ERROR: [youtube] abc: Video unavailable\n"
        )

        self.assertIsInstance(error, CookieError)
        self.assertEqual(str(error), "ERROR: [youtube] abc: Video unavailable")

    def test_file_not_downloaded(self) -> None:
        """ A missing file is not a problem with cookies """
        error = self.download_error(0, "")

        self.assertEqual(str(error), "File ytdl:youtube:abc not downloaded")
        self.assertNotIsInstance(error, CookieError)

    def test_plugin_skips_other_movie_type(self) -> None:
        """ A movie for another plugin is not handled """
        self.assertIsNone(YouTubeDlPlugin(self.configuration).download_movie(MagicMock()))


if __name__ == "__main__":
    unittest.main()
