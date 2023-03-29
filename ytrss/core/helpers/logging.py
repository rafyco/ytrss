import logging

from typing import Dict

_GREY = "\x1b[38;20m"
_BLUE = "\x1b[38;5;39m"
_YELLOW = "\x1b[33;20m"
_RED = "\x1b[31;20m"
_BOLD_RED = "\x1b[31;1m"
_RESET = "\x1b[0m"


class BaseFormatter(logging.Formatter):
    """
    Default formatter
    """
    def __init__(self, message_schema: str) -> None:
        self._formats: Dict[int, str] = {
            logging.DEBUG: f"{_BLUE}{message_schema}{_RESET}",
            logging.INFO: f"{_RESET}{message_schema}{_RESET}",
            logging.WARNING: f"{_YELLOW}{message_schema}{_RESET}",
            logging.ERROR: f"{_RED}{message_schema}{_RESET}",
            logging.CRITICAL: f"{_BOLD_RED}{message_schema}{_RESET}",
        }
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class DebugFormatter(BaseFormatter):
    """
    Logging formatter for logs in debug mode
    """

    def __init__(self) -> None:
        super().__init__("[%(name)s] %(levelname)s - %(message)s (\"%(pathname)s:%(lineno)d\")")


class ClientFormatter(BaseFormatter):
    """
    Logging formatter for logs in client app
    """

    def __init__(self) -> None:
        super().__init__("%(message)s")


logger = logging.getLogger("ytrss")
