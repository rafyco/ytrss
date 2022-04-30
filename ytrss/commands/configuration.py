from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.configuration import Configuration
from ytrss.core.helpers.logging import logger


class ConfigurationCommand(BaseCommand):
    """
    Print configuration
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "configuration")

    def run(self, configuration: Configuration, options: Namespace) -> int:
        logger.info(configuration)
        return 0
