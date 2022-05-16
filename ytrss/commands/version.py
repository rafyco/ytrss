from argparse import Namespace
from youtube_dl.version import __version__ as youtube_dl_version

from ytrss.core.version import Version
from ytrss.commands import BaseCommand
from ytrss.core.helpers.logging import logger


class VersionCommand(BaseCommand):
    """
    Show version of this program
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "version")

    def run(self, options: Namespace) -> int:
        logger.info("ytrss: %s", Version().version)
        logger.info("youtube_dl: %s", youtube_dl_version)
        return 0
