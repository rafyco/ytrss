from ytrss.configuration.entity.source import Source
from ytrss.controlers.youtube.source_downloader import YouTubeSourceDownloader
from ytrss.core.factory import BaseFactory
from ytrss.download.source_downloader import SourceDownloader


class SourceDownloaderFactory(BaseFactory[Source, SourceDownloader]):

    @classmethod
    def build(cls, param: Source) -> SourceDownloader:
        return YouTubeSourceDownloader(param)


create_source_downloader = SourceDownloaderFactory()
