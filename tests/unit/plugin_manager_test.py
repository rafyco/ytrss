"""
Tests of downloading a movie by plugin manager.
"""

import unittest
from typing import List, Optional
from unittest.mock import MagicMock

from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.movie import Movie
from ytrss.core.entity.plugin import Plugin
from ytrss.core.helpers.exceptions import CacheError, DownloadMovieError
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

    def test_cache_error_is_passed_on(self) -> None:
        """ CacheError stops the loop and keeps its message """
        next_plugin = StubPlugin()
        manager = create_manager([StubPlugin(error=CacheError("ERROR: Video unavailable")), next_plugin])

        with self.assertRaisesRegex(CacheError, "ERROR: Video unavailable"):
            manager.download_movie(MagicMock())
        self.assertFalse(next_plugin.called)

    def test_download_movie_error_moves_to_next_plugin(self) -> None:
        """ Plain DownloadMovieError means that plugin does not handle the movie """
        downloaded_movie = MagicMock()
        manager = create_manager([
            StubPlugin(error=DownloadMovieError("YouTubeMovie instance not exists")),
            StubPlugin(result=downloaded_movie)
        ])

        self.assertIs(manager.download_movie(MagicMock()), downloaded_movie)

    def test_no_plugin_can_download(self) -> None:
        """ CacheError is raised when no plugin works """
        manager = create_manager([StubPlugin(), StubPlugin(error=DownloadMovieError("not for this plugin"))])

        with self.assertRaisesRegex(CacheError, "No plugin can download this movie"):
            manager.download_movie(MagicMock())


if __name__ == "__main__":
    unittest.main()
