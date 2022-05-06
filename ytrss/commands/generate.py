from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.managers.destination_manager import DestinationManager


class GenerateCommand(BaseCommand):
    """
    Generate elements in destinations.
    """
    def __init__(self) -> None:
        BaseCommand.__init__(self, "generate")

    def run(self, configuration: YtrssConfiguration, options: Namespace) -> int:
        destination_manager: DestinationManager = configuration.destination_manager

        for destination in destination_manager.destinations:
            destination.on_finish()

        return 0
