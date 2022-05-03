from typing import Sequence, Callable, Optional

from ytrss.configuration.configuration import Configuration
from ytrss.plugins.youtube_dl.youtube_downloader import YouTubeDownloader
from ytrss.core.entity.downloader import Downloader
from ytrss.core.factory import BaseFactory


class DownloadFactory(BaseFactory[Configuration, Downloader]):

    @property
    def plugins(self) -> Sequence[Callable[[Configuration], Optional[Downloader]]]:
        return [
            YouTubeDownloader
        ]


create_downloader = DownloadFactory()
