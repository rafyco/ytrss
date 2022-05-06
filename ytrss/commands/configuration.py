from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.helpers.logging import logger


class ConfigurationCommand(BaseCommand):
    """
    Print configuration
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "configuration")

    def run(self, configuration: YtrssConfiguration, options: Namespace) -> int:
        logger.info("subscriptions:")
        for source in configuration.sources:
            logger.info("\t%s [%s]%s (%s)",
                        source.name,
                        source.url,
                        " [disabled]" if not source.enable else "",
                        source.destination)

        logger.info("\ndestinations:")
        for destination in configuration.destination_manager.destinations:
            logger.info("\t[%s] => %s", destination.identity, destination.info.title)
        return 0
