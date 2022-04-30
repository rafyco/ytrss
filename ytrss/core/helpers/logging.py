import logging

from typing import Dict

_GREY = "\x1b[38;20m"
_BLUE = "\x1b[38;5;39m"
_YELLOW = "\x1b[33;20m"
_RED = "\x1b[31;20m"
_BOLD_RED = "\x1b[31;1m"
_RESET = "\x1b[0m"


class DebugFormatter(logging.Formatter):
    """
    Logging formatter for logs in debug mode
    """

    _message_schema = "[%(name)s] %(levelname)s - %(message)s (\"%(pathname)s:%(lineno)d\")"

    _FORMATS: Dict[int, str] = {
        logging.DEBUG: f"{_BLUE}{_message_schema}{_RESET}",
        logging.INFO: f"{_RESET}{_message_schema}{_RESET}",
        logging.WARNING: f"{_YELLOW}{_message_schema}{_RESET}",
        logging.ERROR: f"{_RED}{_message_schema}{_RESET}",
        logging.CRITICAL: f"{_BOLD_RED}{_message_schema}{_RESET}",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class ClientFormatter(logging.Formatter):
    """
    Logging formatter for logs in client app
    """

    _message_schema = "%(message)s"

    _FORMATS: Dict[int, str] = {
        logging.DEBUG: f"{_BLUE}{_message_schema}{_RESET}",
        logging.INFO: f"{_RESET}{_message_schema}{_RESET}",
        logging.WARNING: f"{_YELLOW}{_message_schema}{_RESET}",
        logging.ERROR: f"{_RED}{_message_schema}{_RESET}",
        logging.CRITICAL: f"{_BOLD_RED}{_message_schema}{_RESET}",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("ytrss")
