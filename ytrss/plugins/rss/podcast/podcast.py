from typing import List

from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.managers.templates_manager import TemplatesManager


class Podcast:
    """
    Class that generate rss file from DownloaderMovie
    """

    def __init__(self, podcast_info: DestinationInfo, templates_manager: TemplatesManager) -> None:
        self.__podcast_info = podcast_info
        self.__items: List[DownloadedMovie] = []
        self._templates_manager = templates_manager

    def add_item(self, movie: DownloadedMovie) -> None:
        """ Add downloaded movie to rss """
        self.__items.append(movie)

    def generate(self) -> str:
        """ Generate rss file for object """
        return self._templates_manager["podcast.xml"]\
            .render(podcast_info=self.__podcast_info, movies=self.__items)
