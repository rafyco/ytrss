import os
import time
from argparse import Namespace

from locks import Mutex

from youtube_dl.version import __version__ as youtube_dl_version

from ytrss.commands.configuration import ConfigurationCommand
from ytrss.commands.version import VersionCommand
from ytrss.commands import BaseCommand
from ytrss.core.algoritms.clean import clean_tasks
from ytrss.core.algoritms.download import download_all_movies
from ytrss.core.algoritms.finder import prepare_urls
from ytrss.core.helpers.logging import logger


class DaemonCommand(BaseCommand):
    """
    Run downloading in loop mode
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "daemon")

    async def run(self, options: Namespace) -> int:

        logger.info("""
 -------------------------------------------------

             /$$
            | $$
 /$$   /$$ /$$$$$$    /$$$$$$   /$$$$$$$ /$$$$$$$
| $$  | $$|_  $$_/   /$$__  $$ /$$_____//$$_____/
| $$  | $$  | $$    | $$  \\__/|  $$$$$$|  $$$$$$
| $$  | $$  | $$ /$$| $$       \\____  $$\\____  $$
|  $$$$$$$  |  $$$$/| $$       /$$$$$$$//$$$$$$$/
 \\____  $$   \\___/  |__/      |_______/|_______/
 /$$  | $$
|  $$$$$$/
 \\______/

 -------------------------------------------------
        """)

        logger.info("")
        await VersionCommand().run(options)
        await ConfigurationCommand().run(options)
        logger.info("")
        while True:
            os.makedirs('/tmp/ytrss', exist_ok=True)
            try:
                with Mutex('/tmp/ytrss/ytrss.lock'):
                    prepare_urls()
                    await download_all_movies()
                    await clean_tasks()
            except BlockingIOError:
                logger.info("Program is already started")
                return 1
            except Exception as ex:  # pylint: disable=W0703
                logger.error("Unexpected daemon problem: %s", str(ex))

            time.sleep(3600)
