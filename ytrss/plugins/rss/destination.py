import io
import os

from ytrss.core.entity.destination import DestinationError
from ytrss.core.managers.templates_manager import TemplatesManager
from ytrss.plugins.default.destination import DefaultDestination

from ytrss.plugins.rss.podcast.podcast import Podcast

from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.core.helpers.logging import logger


class RssDestination(DefaultDestination):
    """
    A destination that create Rss feed.
    """

    def __init__(self, info: DestinationInfo) -> None:
        # pylint: disable=C0123
        if type(self) == RssDestination and info.type != 'rss':
            raise DestinationError()
        DefaultDestination.__init__(self, info)

    def on_finish(self, templates_manager: TemplatesManager) -> None:
        if self.info.output_path is None:
            raise KeyError
        if os.path.isdir(self.info.output_path):
            logger.info("Generate RSS: %s", self.info.title)
            podcast = Podcast(self.info, templates_manager)
            for movie in self.saved_movies:
                logger.debug(" > %s", movie.title)
                try:
                    podcast.add_item(movie=movie)
                except ValueError:
                    logger.info("Cannot add item to rss [%s] %s", movie.identity, movie.title)
            podcast_file = os.path.join(self.info.output_path, "podcast.xml")
            logger.debug("Create rss file: \"%s\"", podcast_file)
            with io.open(podcast_file, "w", encoding="utf-8") as file_handler:
                file_handler.write(podcast.generate())
