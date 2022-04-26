import abc
from argparse import ArgumentParser, Namespace

from ytrss.configuration.configuration import Configuration


class BaseCommand(metaclass=abc.ABCMeta):

    def __init__(self, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    def run(self, configuration: Configuration, options: Namespace) -> int:
        pass

    def arg_parser(self, parser: ArgumentParser) -> None:
        pass

    def __call__(self, configuration: Configuration, options: Namespace) -> int:
        return self.run(configuration, options)
