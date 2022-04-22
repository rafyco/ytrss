from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.core.destination_manager import DestinationManager


class GenerateCommand(BaseCommand):
    """
    Generate elements in destinations.
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "generate")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        destination_manager: DestinationManager = configuration.conf.destination_manager

        for destination in destination_manager.destinations:
            destination.generate_output()

        return 0
