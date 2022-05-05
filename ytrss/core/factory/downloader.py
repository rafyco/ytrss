from typing import Sequence, Callable, Optional

from ytrss.configuration.configuration import Configuration
from ytrss.plugins.youtube_dl.youtube_downloader import YouTubeDownloader
from ytrss.core.entity.downloader import Downloader
from ytrss.core.factory import BaseFactory


class DownloadFactory(BaseFactory[Configuration, Downloader]):
    """
    Factory for Download object
    """

    @property
    def plugins(self) -> Sequence[Callable[[Configuration], Optional[Downloader]]]:
        """ A list of functions that try to produce an object """
        return [
            YouTubeDownloader
        ]


create_downloader = DownloadFactory()
