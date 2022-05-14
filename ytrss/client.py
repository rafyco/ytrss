#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import logging
import sys
from argparse import ArgumentParser
from typing import Optional, Sequence, List

from ytrss.commands import BaseCommand
from ytrss.commands.configuration import ConfigurationCommand
from ytrss.commands.download import DownloadCommand
from ytrss.commands.generate import GenerateCommand
from ytrss.commands.run import RunCommand
from ytrss.commands.url import UrlCommand
from ytrss.commands.version import VersionCommand
from ytrss.configuration.configuration import ConfigurationFileNotExistsError, ConfigurationError
from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.configuration.factory import create_configuration
from ytrss.core.helpers.logging import DebugFormatter, ClientFormatter, logger
from ytrss.core.helpers.string_utils import first_line
from ytrss.core.managers.manager_service import default_manager_service

__subcommands__: List[BaseCommand] = [
    VersionCommand(),
    RunCommand(),
    GenerateCommand(),
    ConfigurationCommand(),
    GenerateCommand(),
    DownloadCommand(),
    UrlCommand()
]


def _option_args() -> ArgumentParser:
    parser = ArgumentParser(description="command line tool to manage ytrss package",
                            prog='ytrss')
    parser.add_argument("-c", "--conf", dest="config_file",
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("-d", "--debug-log", dest="log_debug",
                        action="store_true", default=False,
                        help="Enable debug logging")

    return parser


def _configure_logging(debug_log: bool) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(DebugFormatter() if debug_log else ClientFormatter())
    logging.basicConfig(
        level=logging.DEBUG if debug_log else logging.INFO,
        handlers=[stream_handler]
    )


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    Main function for command line program.
    """
    parser = _option_args()

    subparsers = parser.add_subparsers(title="commands", description="Use once of this commands", dest="command")
    subparsers.add_parser("help", help="Print help message")
    for command in __subcommands__:
        subparser = subparsers.add_parser(command.name, help=first_line(command.__doc__))
        command.arg_parser(subparser)

    options = parser.parse_args(argv)

    _configure_logging(options.log_debug)

    try:
        manager_service = default_manager_service()
        manager_service.configuration = YtrssConfiguration(create_configuration("ytrss", options.config_file))
    except ConfigurationFileNotExistsError:
        logger.warning("Configuration file not exists")
        sys.exit(1)
    except ConfigurationError as ex:
        logger.debug("%s: %s", type(ex), ex)
        logger.error("There are no configuration file")
        sys.exit(2)

    try:
        # pylint: disable=C0415
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    if options.command is None or options.command == "help":
        parser.print_help()
        sys.exit(0)

    for command in __subcommands__:
        if command.name == options.command:
            sys.exit(command(options))

    logger.error("command: %s", options.command)


if __name__ == "__main__":
    main()
