from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.core.helpers.logging import logger


class ConfigurationCommand(BaseCommand):
    """
    Print configuration
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "configuration")

    def run(self, options: Namespace) -> int:
        logger.info("subscriptions:")
        for source in self.manager_service.configuration.sources:
            logger.info("\t%s [%s]%s (%s)",
                        source.name,
                        source.url,
                        " [disabled]" if not source.enable else "",
                        source.destination)

        logger.info("\ndestinations:")
        for destination in self.manager_service.destination_manager.destinations:
            logger.info("\t[%s] => %s", destination.identity, destination.info.title)

        logger.info("\nplugins:")
        for plugin in self.manager_service.plugin_manager.plugins:
            logger.info("\t[%s] => %s", plugin.plugin_name, plugin.plugin_description)
        return 0
