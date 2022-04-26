from ytrss.configuration.configuration import Configuration
from ytrss.controlers.youtube_dl.youtube_downloader import YouTubeDownloader
from ytrss.core.entity.downloader import Downloader
from ytrss.core.factory import BaseFactory


class DownloadFactory(BaseFactory[Configuration, Downloader]):
    """
    Factory for Downloaders
    """

    @classmethod
    def build(cls, param: Configuration) -> Downloader:
        """
        Build defined object from parameter
        """
        return YouTubeDownloader(param)


create_downloader = DownloadFactory()
