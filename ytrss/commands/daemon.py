import asyncio
from datetime import datetime
from argparse import Namespace

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore[import-untyped]

from ytrss.commands.configuration import ConfigurationCommand
from ytrss.commands.version import VersionCommand
from ytrss.commands import BaseCommand
from ytrss.core.entity.webhooks import StartDaemonWebhook
from ytrss.core.helpers.logging import logger
from ytrss.core.algoritms.run import run_one_step


class DaemonCommand(BaseCommand):
    """
    Run downloading in loop mode
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "daemon")

    async def run(self, options: Namespace) -> int:

        self.manager_service.webhook_manager.invoke_hook(StartDaemonWebhook())

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

        scheduler = AsyncIOScheduler()

        scheduler.add_job(
            run_one_step,
            'interval',
            hours=1,
            next_run_time=datetime.now(),
        )

        scheduler.start()
        logger.info("Scheduler started")

        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Shutting down scheduler...")
        finally:
            scheduler.shutdown()

        return 0
