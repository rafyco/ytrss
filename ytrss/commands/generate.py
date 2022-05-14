from argparse import Namespace

from ytrss.commands import BaseCommand


class GenerateCommand(BaseCommand):
    """
    Generate elements in destinations.
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "generate")

    def run(self, options: Namespace) -> int:
        for destination in self.manager_service.destination_manager.destinations:
            destination.on_finish(self.manager_service.templates_manager)
        return 0
