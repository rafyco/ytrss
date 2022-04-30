from argparse import Namespace
from youtube_dl.version import __version__ as youtube_dl_version

import ytrss
from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.core.helpers.logging import logger


class VersionCommand(BaseCommand):
    """
    Show version of this program
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "version")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        logger.info("%s: %s", ytrss.__name__, ytrss.__version__)
        logger.info("youtube_dl: %s", youtube_dl_version)
        return 0
