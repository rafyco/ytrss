import unittest

from ytrss.configuration.entity.source import Source
from ytrss.plugins.youtube.youtube_channel_source_downloader import YouTubeChannelSourceDownloader
from ytrss.plugins.youtube.youtube_named_channel_source_downloader import \
    YouTubeNamedChannelSourceDownloader
from ytrss.plugins.youtube.youtube_playlist_source_downloader import YouTubePlaylistSourceDownloader


class TestFinder(unittest.TestCase):  # pylint: disable=R0904
    """ Test of finder """

    def test_channel_with_code_find(self) -> None:
        """ Test channel finder with code. """
        source = YouTubeChannelSourceDownloader(Source.from_json(dict(
            url="https://www.youtube.com/channel/UC5SdvjkYXdGAqmqAGlxTnpw",
            destination="default",
        )))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie, _ in movies:
            print(f"url: {movie}")
            self.assertTrue(movie.url is not None
                            and movie.url.startswith("https://www.youtube.com/watch?v="))

    def test_channel_with_name_find(self) -> None:
        """ Test channel finder with name. """
        source = YouTubeNamedChannelSourceDownloader(Source.from_json(dict(
            url="https://www.youtube.com/c/MinnivaOfficial",
            destination="default",
        )))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie, _ in movies:
            print(f"url: {movie}")
            self.assertTrue(movie.url is not None
                            and movie.url.startswith("https://www.youtube.com/watch?v="))

    def test_playlist_find(self) -> None:
        """ Test playlist finder. """
        source = YouTubePlaylistSourceDownloader(Source.from_json(dict(
            url="https://www.youtube.com/playlist?list=PL6ZLc-zZUnxlkB9t8CcpFZeV6V5I_cVgu",
            destination="default",
        )))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie, _ in movies:
            print(f"url: {movie}")
            self.assertTrue(movie.url is not None
                            and movie.url.startswith("https://www.youtube.com/watch?v="))
