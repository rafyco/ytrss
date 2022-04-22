#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import logging
import sys
from argparse import ArgumentParser
from typing import Optional, Sequence, List

from ytrss.commands import BaseCommand
from ytrss.commands.configuration import ConfigurationCommand
from ytrss.commands.generate import GenerateCommand
from ytrss.commands.run import RunCommand
from ytrss.commands.url import UrlCommand
from ytrss.commands.version import VersionCommand
from ytrss.configuration.configuration import ConfigurationFileNotExistsError, ConfigurationError
from ytrss.configuration.factory import configuration_factory
from ytrss.core.string_utils import first_line

__subcommands__: List[BaseCommand] = [
    RunCommand(),
    GenerateCommand(),
    ConfigurationCommand(),
    GenerateCommand(),
    UrlCommand(),
    VersionCommand()
]


def __option_args() -> ArgumentParser:
    """
    Parsing argument for command line program.
    """
    parser = ArgumentParser(description="command line tool to manage ytrss package",
                            prog='ytrss')
    parser.add_argument("-c", "--conf", dest="config_file",
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("-l", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        help="Set the logging level")

    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    Main function for command line program.
    """
    parser = __option_args()

    subparsers = parser.add_subparsers(title="commands", description="Use once of this commands", dest="command")
    for command in __subcommands__:
        subparser = subparsers.add_parser(command.name, help=first_line(command.__doc__))
        command.arg_parser(subparser)

    options = parser.parse_args(argv)

    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)

    try:
        configuration = configuration_factory(options.config_file)
    except ConfigurationFileNotExistsError:
        print("File not exists")
        sys.exit(1)
    except ConfigurationError as ex:
        logging.debug("%s: %s", type(ex), ex)
        sys.exit(2)

    try:
        # pylint: disable=C0415
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    if options.command is None:
        parser.print_help()
        sys.exit(0)

    for command in __subcommands__:
        if command.name == options.command:
            sys.exit(command(configuration, options))

    logging.error("command: %s", options.command)


if __name__ == "__main__":
    main()
