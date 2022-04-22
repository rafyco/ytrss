from argparse import Namespace
from youtube_dl.version import __version__ as youtube_dl_version

import ytrss
from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration


class VersionCommand(BaseCommand):
    """
    Show version of this program
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "version")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        print(f"{ytrss.__name__}: {ytrss.__version__}")
        print(f"youtube_dl: {youtube_dl_version}")
        return 0
