import abc
from argparse import ArgumentParser, Namespace

from ytrss.configuration.configuration import Configuration


class BaseCommand(metaclass=abc.ABCMeta):
    """
    Base object of command
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    def run(self, configuration: Configuration, options: Namespace) -> int:
        """
        Run command
        """

    def arg_parser(self, parser: ArgumentParser) -> None:
        """
        Configures commands argument parser.
        """

    def __call__(self, configuration: Configuration, options: Namespace) -> int:
        return self.run(configuration, options)
