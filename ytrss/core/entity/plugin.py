import abc

from typing import Optional

from ytrss.core.entity.downloader import Downloader

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.destination import Destination

from ytrss.configuration.entity.destination_info import DestinationInfo

from ytrss.core.entity.movie import Movie
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.helpers.string_utils import first_line

from ytrss.core.helpers.typing import Url


class BasePlugin(metaclass=abc.ABCMeta):
    """ Plugin's interface """

    @property
    def plugin_name(self) -> str:
        """ Plugin's name """
        return type(self).__name__

    @property
    def plugin_description(self) -> str:
        """ Short description of plugin """
        short_desc = first_line(self.__doc__)
        return short_desc if short_desc != "" else f"{self.plugin_name}: not description"

    @abc.abstractmethod
    def create_movie(self, url: Url) -> Optional[Movie]:
        """ Method that creates a Movie object."""

    @abc.abstractmethod
    def create_destination(self, info: DestinationInfo) -> Optional[Destination]:
        """ Method that creates destination object. """

    @abc.abstractmethod
    def create_downloader(self, movie: Movie, configuration: YtrssConfiguration) -> Optional[Downloader]:
        """ Method that creates a downloader object. """

    @abc.abstractmethod
    def create_source_downloader(self, source: Source) -> Optional[SourceDownloader]:
        """ Method that creates a source downloader object. """

    @abc.abstractmethod
    def modify_res_files(self, downloaded_movie: DownloadedMovie) -> None:
        """ Method that modify downloaded files. """


class Plugin(BasePlugin):
    """ An implementation of plugin that not return any of new objects.

    This object can be used to implement new plugin object. All method that creates objects, return None.
    """

    def create_destination(self, info: DestinationInfo) -> Optional[Destination]:
        return None

    def create_downloader(self, movie: Movie, configuration: YtrssConfiguration) -> Optional[Downloader]:
        return None

    def create_source_downloader(self, source: Source) -> Optional[SourceDownloader]:
        return None

    def create_movie(self, url: Url) -> Optional[Movie]:
        return None

    def modify_res_files(self, downloaded_movie: DownloadedMovie) -> None:
        pass
