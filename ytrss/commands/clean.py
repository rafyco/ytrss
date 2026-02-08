from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.core.algoritms.clean import clean_tasks


class CleanCommand(BaseCommand):
    """
    Clean all unnecessary files.
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "clean")

    async def run(self, options: Namespace) -> int:
        await clean_tasks()
        return 0
