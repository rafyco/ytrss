from ytrss.configuration.entity.source import Source
from ytrss.controlers.youtube.source_downloader import YouTubeSourceDownloader
from ytrss.download.source_downloader import SourceDownloader


def create_source_downloader(source: Source) -> SourceDownloader:
    """
    Create source downloader object from args
    """
    return YouTubeSourceDownloader(source)
