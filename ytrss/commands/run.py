import os
from argparse import Namespace

from locks import Mutex

from ytrss.commands import BaseCommand
from ytrss.core.algoritms.clean import clean_tasks
from ytrss.core.algoritms.download import download_all_movies
from ytrss.core.algoritms.finder import prepare_urls
from ytrss.core.helpers.logging import logger


class RunCommand(BaseCommand):
    """
    Find movie from sources and download
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "run")

    async def run(self, options: Namespace) -> int:
        os.makedirs('/tmp/ytrss', exist_ok=True)
        try:
            with Mutex('/tmp/ytrss/ytrss.lock'):
                prepare_urls()
                await download_all_movies()
                await clean_tasks()
        except BlockingIOError:
            logger.info("Program is already started")
            return 1
        return 0
