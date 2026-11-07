"""
Tests of downloading a movie by plugin manager.
"""

import unittest
from typing import List, Optional
from unittest.mock import MagicMock

from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.movie import Movie, MovieError
from ytrss.core.entity.plugin import Plugin
from ytrss.core.helpers.exceptions import CookieError, DownloadMovieError
from ytrss.core.helpers.typing import Url
from ytrss.core.managers.plugin_manager import PluginManager


class StubPlugin(Plugin):
    """ A plugin that raises an error or returns a downloaded movie """

    def __init__(
            self,
            error: Optional[Exception] = None,
            result: Optional[DownloadedMovie] = None,
            movie: Optional[Movie] = None
    ) -> None:
        self.error = error
        self.result = result
        self.movie = movie
        self.called = False

    def download_movie(self, movie: Movie) -> Optional[DownloadedMovie]:
        self.called = True
        if self.error is not None:
            raise self.error
        return self.result

    def create_movie(self, url: Url) -> Optional[Movie]:
        self.called = True
        if self.error is not None:
            raise self.error
        return self.movie


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


class TestPluginManagerCreateMovie(unittest.TestCase):
    """
    Tests of PluginManager.create_movie
    """

    def test_movie_error_keeps_its_message(self) -> None:
        """ The text of the last MovieError is passed on, when no plugin can create a movie """
        cause = MovieError("ERROR: Video unavailable")
        manager = create_manager([StubPlugin(error=MovieError("first")), StubPlugin(error=cause), StubPlugin()])

        with self.assertRaisesRegex(MovieError, "^ERROR: Video unavailable$") as context:
            manager.create_movie(Url("https://example.com"))
        self.assertIs(context.exception.__cause__, cause)

    def test_movie_error_moves_to_next_plugin(self) -> None:
        """ MovieError of one plugin does not stop the others """
        movie = MagicMock()
        manager = create_manager([StubPlugin(error=MovieError("broken")), StubPlugin(movie=movie)])

        self.assertIs(manager.create_movie(Url("https://example.com")), movie)

    def test_no_plugin_can_create(self) -> None:
        """ MovieError is raised when no plugin reports anything """
        manager = create_manager([StubPlugin(), StubPlugin(error=ValueError("broken"))])

        with self.assertRaisesRegex(MovieError, "^$"):
            manager.create_movie(Url("https://example.com"))


if __name__ == "__main__":
    unittest.main()
