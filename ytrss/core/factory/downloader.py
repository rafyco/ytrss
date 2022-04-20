from ytrss.configuration.configuration import Configuration
from ytrss.controlers.youtube_dl.youtube_downloader import YouTubeDownloader
from ytrss.core.entity.downloader import Downloader


def create_downloader(configuration: Configuration) -> Downloader:
    """
    Factory of downloader object
    """
    return YouTubeDownloader(configuration)
