import unittest

from ytrss.configuration.entity.source import Source
from ytrss.controlers.youtube.source_downloader import YouTubeSourceDownloader


class TestFinder(unittest.TestCase):  # pylint: disable=R0904
    """ Test of finder """

    def test_user_find(self) -> None:
        """ Test user finder. """
        source = YouTubeSourceDownloader(Source.from_json(dict(code="UCViVL2aOkLWKcFVi0_p6u6g",
                                                               destination="default")))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie in movies:
            print(f"url: {movie}")
            self.assertIsNotNone(movie.url)
            self.assertTrue(movie.url is not None
                            and movie.url.startswith("https://www.youtube.com/watch?v="))

    def test_playlist_find(self) -> None:
        """ Test playlist finder. """
        source = YouTubeSourceDownloader(Source.from_json(dict(
            code="PLgVGo5sYBI-QeaAlxmJvw0Spw63nohIq6",
            destination="default",
            type="playlist"
        )))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie in movies:
            print(f"url: {movie}")
            self.assertTrue(movie.url is not None
                            and movie.url.startswith("https://www.youtube.com/watch?v="))
