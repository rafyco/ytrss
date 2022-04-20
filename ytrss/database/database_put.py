import abc

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie


class DatabasePut(metaclass=abc.ABCMeta):
    """
    TODO: documentation
    """

    @abc.abstractmethod
    def queue_mp3(self, movie: Movie, destination: DestinationId) -> bool:
        """
        TODO: documentation
        """
