import abc

from ytrss.core.entity.downloaded_movie import DownloadedMovie


class DownloaderError(Exception):
    """
    Error in Downloaders.
    """


class Downloader(metaclass=abc.ABCMeta):
    """ An abstract class of downloader

    The class represents an object that can download movie. It should return a sequence of paths to
    objects that has an information about files.
    """

    @abc.abstractmethod
    def download(self) -> DownloadedMovie:
        """
        Download movie

        The method which should download movie and return a DownloadedMovie object.
        """
