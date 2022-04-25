import os
from argparse import Namespace

from locks import Mutex

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.core.logging import logger
from ytrss.download.algoritms import download_all_movies
from ytrss.finder.algoritms import prepare_urls


class RunCommand(BaseCommand):
    """
    Find movie from sources and download
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "run")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        os.makedirs('/tmp/ytrss', exist_ok=True)
        try:
            with Mutex('/tmp/ytrss/ytrss.lock'):
                prepare_urls(configuration)
                download_all_movies(configuration)
        except BlockingIOError:
            logger.info("Program is already started")
            return 1
        return 0
