import abc
from dataclasses import dataclass

from ytrss.core.entity.movie import Movie


@dataclass
class WebhookType(metaclass=abc.ABCMeta):
    """ An abstract class representing a webhook """
    name: str
    data: dict[str, str]


class StartDaemonWebhook(WebhookType):
    """ A webhook class representing a start daemon """

    def __init__(self) -> None:
        super().__init__('start-daemon', {})


class FoundNewMovieWebhook(WebhookType):
    """ A webhook class representing a found new movie """
    def __init__(self, movie: Movie, destination: str) -> None:
        super().__init__('found-new-movie', {
            'title': movie.title,
            'url': movie.url,
            'id': movie.identity,
            'desc': movie.description,
            'destination': destination
        })


class StartDownloadingMovieWebhook(WebhookType):
    """ A webhook class representing a start downloading movie """
    def __init__(self, movie: Movie) -> None:
        super().__init__('start-downloading-movie', {
            'title': movie.title,
            'url': movie.url,
            'id': movie.identity,
            'desc': movie.description
        })


class SuccessDownloadMovieWebhook(WebhookType):
    """ A webhook class representing a download movie """
    def __init__(self, movie: Movie) -> None:
        super().__init__('success-download-movie', {
            'title': movie.title,
            'url': movie.url,
            'id': movie.identity,
            'desc': movie.description
        })


class FailedDownloadMovieWebhook(WebhookType):
    """ A webhook class representing a failed downloaded movie """
    def __init__(self, movie: Movie, cause: Exception) -> None:
        super().__init__('failed-download-movie', {
            'title': movie.title,
            'url': movie.url,
            'id': movie.identity,
            'desc': movie.description,
            'cause': str(cause)
        })
