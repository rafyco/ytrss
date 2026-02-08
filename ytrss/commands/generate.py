from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.core.algoritms.generate import generate


class GenerateCommand(BaseCommand):
    """
    Generate elements in destinations.
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "generate")

    async def run(self, options: Namespace) -> int:
        await generate(self.manager_service)
        return 0
