import os
from datetime import datetime
from locks import Mutex

from ytrss.core.algoritms.clean import clean_tasks
from ytrss.core.algoritms.download import download_all_movies
from ytrss.core.algoritms.finder import prepare_urls
from ytrss.core.helpers.logging import logger


async def run_one_step() -> bool:
    """
    Run one step of algoritm

    Prepare new urls, download all movies and clear old tasks in one step.
    """
    os.makedirs('/tmp/ytrss', exist_ok=True)
    try:
        with Mutex('/tmp/ytrss/ytrss.lock'):
            logger.info("Start process: %s", datetime.now())
            prepare_urls()
            await download_all_movies()
            await clean_tasks()
            logger.info("Stop process: %s", datetime.now())
            return True
    except BlockingIOError:
        logger.info("Program is already started")
    except Exception as ex:  # pylint: disable=W0703
        logger.error("Unexpected daemon problem: %s", str(ex))
    return False
