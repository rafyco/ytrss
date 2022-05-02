import abc
from argparse import ArgumentParser, Namespace

from ytrss.configuration.configuration import Configuration


class BaseCommand(metaclass=abc.ABCMeta):
    """ Abstract class represents a command in terminal client """

    def __init__(self, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    def run(self, configuration: Configuration, options: Namespace) -> int:
        """ A main work that be done in subcommand from terminal client """

    def arg_parser(self, parser: ArgumentParser) -> None:
        """ Parse argument

        In this method terminal arguments from subcommand should be registered in main subparser.
        """

    def __call__(self, configuration: Configuration, options: Namespace) -> int:
        return self.run(configuration, options)
