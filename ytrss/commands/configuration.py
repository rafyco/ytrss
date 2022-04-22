from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration


class ConfigurationCommand(BaseCommand):
    """
    Print configuration
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "configuration")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        print(configuration)
        return 0
