"""
Tests of movie-error webhook and the error cache.
"""

import asyncio
import os
import sqlite3
import tempfile
import unittest
from typing import List, Tuple
from unittest.mock import MagicMock, patch

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.algoritms.download import download_all_movies, download_task, report_movie_error
from ytrss.core.entity.movie import Movie, MovieError
from ytrss.core.entity.webhooks import MovieErrorData, MovieErrorWebhook
from ytrss.core.helpers.exceptions import DownloadMovieError
from ytrss.core.helpers.string_utils import error_type
from ytrss.database.sqlite.sqlite_database import SqliteDatabase

FIRST = DestinationId("first")
SECOND = DestinationId("second")
UNAVAILABLE = "ERROR: [youtube] abc: Video unavailable"
PRIVATE = "ERROR: [youtube] abc: Private video"


def create_movie(identity: str) -> MagicMock:
    """ Create a movie that is ready to download """
    movie = MagicMock(spec=Movie)
    movie.identity = identity
    movie.url = f"https://example.com/{identity}"
    movie.title = f"title {identity}"
    movie.description = "description"
    movie.is_ready = True
    return movie


class TestErrorType(unittest.TestCase):
    """
    Tests of error_type
    """

    def test_youtube_line(self) -> None:
        """ Prefixes of yt_dlp are removed """
        self.assertEqual(error_type("ERROR: [youtube] dQw4w-9_XcQ: Video unavailable"), "Video unavailable")

    def test_last_error_line(self) -> None:
        """ Only the last error counts, warnings are ignored """
        cause = "WARNING: [youtube] abc: old\nERROR: first\nERROR: [youtube:tab] UCabc: Sign in\n"
        self.assertEqual(error_type(cause), "Sign in")

    def test_two_movies_give_one_type(self) -> None:
        """ Id of movie and numbers don't change the type """
        self.assertEqual(
            error_type("ERROR: [youtube] abc: Available in 3 days from 2026"),
            error_type("ERROR: [youtube] xyz: Available in 12 days from 2027")
        )

    def test_error_after_text_of_movie_creation(self) -> None:
        """ Url in the text of YouTubeMovie error is not a part of the type """
        self.assertEqual(
            error_type("Invalid address type: [https://example.com/a] -> ERROR: [youtube] a: Video unavailable\n"),
            error_type("Invalid address type: [https://example.com/b] -> ERROR: [youtube] b: Video unavailable\n")
        )

    def test_message_without_error_mark(self) -> None:
        """ The first line is used when there is no ERROR mark """
        self.assertEqual(error_type("\nFile not saved 12\nsecond line"), "File not saved #")

    def test_length(self) -> None:
        """ Type is cut to 200 characters """
        self.assertEqual(len(error_type(f"ERROR: {'a' * 300}")), 200)


class TestMovieErrorWebhook(unittest.TestCase):
    """
    Tests of MovieErrorWebhook
    """

    keys = {"title", "url", "id", "desc", "destination", "error_type", "cause"}

    def test_with_data(self) -> None:
        """ Data of error are sent """
        error = MovieErrorData("first", "cause", "https://example.com/a", "a", "title", "description")
        self.assertEqual(MovieErrorWebhook(error, "type").data, {
            "title": "title",
            "url": "https://example.com/a",
            "id": "a",
            "desc": "description",
            "destination": "first",
            "error_type": "type",
            "cause": "cause"
        })

    def test_without_movie(self) -> None:
        """ All keys exist without movie, because webhook url can use any of them """
        data = MovieErrorWebhook(MovieErrorData("first", "cause"), "type").data
        self.assertEqual(set(data), self.keys)
        self.assertEqual(data["title"], "")
        self.assertEqual(data["url"], "")


class MovieErrorTestCase(unittest.TestCase):
    """
    Base with a sqlite database in temp folder and a mocked WebhookManager
    """

    def setUp(self) -> None:
        folder = tempfile.TemporaryDirectory()  # pylint: disable=R1732
        self.addCleanup(folder.cleanup)
        self.db_file = os.path.join(folder.name, "ytrss.db")
        configuration = MagicMock()
        configuration.database_path = folder.name
        self.plugin_manager = MagicMock()
        self.database = SqliteDatabase(configuration, self.plugin_manager)
        self.manager_service = MagicMock()
        self.manager_service.database = self.database

    @property
    def hooks(self) -> List[MovieErrorWebhook]:
        """ Invoked movie-error webhooks """
        calls = self.manager_service.webhook_manager.invoke_hook.call_args_list
        return [call.args[0] for call in calls if isinstance(call.args[0], MovieErrorWebhook)]

    @property
    def stored_errors(self) -> List[Tuple[str, str]]:
        """ Rows of the error cache """
        conn = sqlite3.connect(self.db_file)
        self.addCleanup(conn.close)
        return conn.execute("SELECT destination, error_type FROM movie_errors").fetchall()


class TestReportMovieError(MovieErrorTestCase):
    """
    Tests of report_movie_error
    """

    def report(self, destination: DestinationId, cause: str) -> None:
        """ Report an error """
        report_movie_error(MovieErrorData(destination, cause), self.manager_service)

    def test_same_error_invokes_hook_once(self) -> None:
        """ Same destination and type give one hook, also for two different movies """
        self.report(FIRST, UNAVAILABLE)
        self.report(FIRST, UNAVAILABLE)
        self.report(FIRST, "ERROR: [youtube] other: Video unavailable")

        self.assertEqual(len(self.hooks), 1)
        self.assertEqual(self.hooks[0].data["destination"], "first")
        self.assertEqual(self.hooks[0].data["error_type"], "Video unavailable")
        self.assertEqual(self.hooks[0].data["cause"], UNAVAILABLE)

    def test_new_type_invokes_hook(self) -> None:
        """ A new type gives another hook """
        self.report(FIRST, UNAVAILABLE)
        self.report(FIRST, PRIVATE)

        self.assertEqual(len(self.hooks), 2)

    def test_other_destination_invokes_hook(self) -> None:
        """ Other destination gives another hook """
        self.report(FIRST, UNAVAILABLE)
        self.report(SECOND, UNAVAILABLE)

        self.assertEqual(len(self.hooks), 2)

    def test_quote_in_error(self) -> None:
        """ Error text with quotes is stored """
        self.report(FIRST, """ERROR: can't "open" it""")

        self.assertEqual(self.stored_errors, [("first", """can't "open" it""")])

    def test_not_ready_movie_is_skipped(self) -> None:
        """ Premieres and live events are not errors """
        self.report(FIRST, "ERROR: [youtube] abc: Premieres in 3 hours")
        self.report(FIRST, "ERROR: [youtube] abc: This live event will begin in 3 hours.")

        self.assertEqual(self.hooks, [])
        self.assertEqual(self.stored_errors, [])


class TestDownloadTask(MovieErrorTestCase):
    """
    Tests of download_task
    """

    def download(self, identity: str, destination: DestinationId, error: Exception | None = None) -> bool:
        """ Run download_task for a new movie, download ends with given error """
        movie = create_movie(identity)
        self.database.queue_mp3(movie, destination)
        with patch("ytrss.core.algoritms.download.download_movie", side_effect=error):
            return asyncio.run(download_task(movie, destination, self.manager_service))

    def test_error_invokes_hook_once(self) -> None:
        """ Failed downloads of two movies give one hook with data of first movie """
        self.assertFalse(self.download("a", FIRST, DownloadMovieError(UNAVAILABLE)))
        self.assertFalse(self.download("b", FIRST, DownloadMovieError(UNAVAILABLE)))

        self.assertEqual(len(self.hooks), 1)
        self.assertEqual(self.hooks[0].data["id"], "a")

    def test_success_clears_only_its_destination(self) -> None:
        """ After a success the same error fires again, but only for that destination """
        self.download("a", FIRST, DownloadMovieError(UNAVAILABLE))
        self.download("b", SECOND, DownloadMovieError(UNAVAILABLE))

        self.assertTrue(self.download("c", FIRST))
        self.assertEqual(self.stored_errors, [("second", "Video unavailable")])

        self.download("d", SECOND, DownloadMovieError(UNAVAILABLE))
        self.assertEqual(len(self.hooks), 2)

        self.download("e", FIRST, DownloadMovieError(UNAVAILABLE))
        self.assertEqual(len(self.hooks), 3)


class TestMoviesOnError(MovieErrorTestCase):
    """
    Tests of errors raised during movie creation
    """

    def setUp(self) -> None:
        super().setUp()
        self.database.queue_mp3(create_movie("a"), FIRST)
        self.database.queue_mp3(create_movie("b"), SECOND)

    def test_on_error_gets_text_and_destination(self) -> None:
        """ on_error gets data of the failing row, and this row is skipped """
        working_movie = create_movie("b")
        error = MovieError(UNAVAILABLE)
        self.plugin_manager.create_movie.side_effect = [error, working_movie]
        on_error = MagicMock()

        movies = list(self.database.movies(on_error))

        self.assertEqual(movies, [(working_movie, SECOND)])
        on_error.assert_called_once_with("a", "https://example.com/a", FIRST, error)

    def test_without_callback(self) -> None:
        """ The row is skipped without any callback too """
        self.plugin_manager.create_movie.side_effect = MovieError(UNAVAILABLE)

        self.assertEqual(list(self.database.movies()), [])

    def test_download_all_movies_invokes_hook_once(self) -> None:
        """ Errors from before the download give one hook for each destination, also on next runs """
        self.plugin_manager.create_movie.side_effect = MovieError(
            f"Invalid address type: [https://example.com/a] -> {UNAVAILABLE}\n"
        )

        asyncio.run(download_all_movies(self.manager_service))
        asyncio.run(download_all_movies(self.manager_service))

        self.assertEqual(len(self.hooks), 2)
        data = self.hooks[0].data
        self.assertEqual(data["id"], "a")
        self.assertEqual(data["url"], "https://example.com/a")
        self.assertEqual(data["destination"], "first")
        self.assertEqual(data["error_type"], "Video unavailable")
        self.assertEqual(data["title"], "")


if __name__ == "__main__":
    unittest.main()
