from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.core.algoritms.run import run_one_step


class RunCommand(BaseCommand):
    """
    Find movie from sources and download
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "run")

    async def run(self, options: Namespace) -> int:
        result = await run_one_step()
        return 0 if result else 1
