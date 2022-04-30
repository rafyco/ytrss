from ytrss.configuration.configuration import Configuration
from ytrss.plugins.youtube_dl.youtube_downloader import YouTubeDownloader
from ytrss.core.entity.downloader import Downloader
from ytrss.core.factory import BaseFactory


class DownloadFactory(BaseFactory[Configuration, Downloader]):

    @classmethod
    def build(cls, param: Configuration) -> Downloader:
        return YouTubeDownloader(param)


create_downloader = DownloadFactory()
