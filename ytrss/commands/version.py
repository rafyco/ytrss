from argparse import Namespace
from yt_dlp.version import __version__ as yt_dlp_version

from ytrss.core.version import Version
from ytrss.commands import BaseCommand
from ytrss.core.helpers.logging import logger


class VersionCommand(BaseCommand):
    """
    Show version of this program
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "version")

    async def run(self, options: Namespace) -> int:
        logger.info("ytrss: %s", Version().version)
        logger.info("yt_dlp: %s", yt_dlp_version)
        return 0
