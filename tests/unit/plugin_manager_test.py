"""
Tests of downloading a movie by plugin manager.
"""

import unittest
from typing import List, Optional
from unittest.mock import MagicMock

from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.movie import Movie
from ytrss.core.entity.plugin import Plugin
from ytrss.core.helpers.exceptions import CookieError, DownloadMovieError
from ytrss.core.managers.plugin_manager import PluginManager


class StubPlugin(Plugin):
    """ A plugin that raises an error or returns a downloaded movie """

    def __init__(self, error: Optional[Exception] = None, result: Optional[DownloadedMovie] = None) -> None:
        self.error = error
        self.result = result
        self.called = False

    def download_movie(self, movie: Movie) -> Optional[DownloadedMovie]:
        self.called = True
        if self.error is not None:
            raise self.error
        return self.result


def create_manager(plugins: List[StubPlugin]) -> PluginManager:
    """ Create a plugin manager that uses only given plugins """
    manager = PluginManager(MagicMock())
    manager._plugins = list(plugins)  # pylint: disable=W0212
    return manager


class TestPluginManagerDownloadMovie(unittest.TestCase):
    """
    Tests of PluginManager.download_movie
    """

    def test_cookie_error_is_passed_on(self) -> None:
        """ CookieError stops the loop and keeps its message """
        next_plugin = StubPlugin()
        manager = create_manager([StubPlugin(error=CookieError("ERROR: Sign in")), next_plugin])

        with self.assertRaisesRegex(CookieError, "ERROR: Sign in"):
            manager.download_movie(MagicMock())
        self.assertFalse(next_plugin.called)

    def test_download_movie_error_is_passed_on(self) -> None:
        """ DownloadMovieError stops the loop and keeps its message """
        next_plugin = StubPlugin()
        manager = create_manager([StubPlugin(error=DownloadMovieError("ERROR: Video unavailable")), next_plugin])

        with self.assertRaisesRegex(DownloadMovieError, "ERROR: Video unavailable"):
            manager.download_movie(MagicMock())
        self.assertFalse(next_plugin.called)

    def test_other_error_moves_to_next_plugin(self) -> None:
        """ An unexpected error of one plugin does not stop the others """
        downloaded_movie = MagicMock()
        manager = create_manager([StubPlugin(error=ValueError("broken")), StubPlugin(result=downloaded_movie)])

        self.assertIs(manager.download_movie(MagicMock()), downloaded_movie)

    def test_no_plugin_can_download(self) -> None:
        """ DownloadMovieError, and not CookieError, is raised when no plugin works """
        manager = create_manager([StubPlugin(), StubPlugin(error=ValueError("broken"))])

        with self.assertRaisesRegex(DownloadMovieError, "No plugin can download this movie") as context:
            manager.download_movie(MagicMock())
        self.assertNotIsInstance(context.exception, CookieError)


if __name__ == "__main__":
    unittest.main()
