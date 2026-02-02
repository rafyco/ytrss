import sys
from io import StringIO, TextIOBase
from typing import Union
import yt_dlp
from ytrss.core.helpers.logging import logger


class _Tee(TextIOBase):
    """
    A TextIO that display elements on screen and save to String
    """
    def __init__(self, is_error: bool = False) -> None:
        self._string = StringIO()
        self._is_error = is_error

    def write(self, obj: str) -> int:
        """
        Write object to stream
        """
        if self._is_error:
            logger.error(obj)
        else:
            logger.info(obj)
        return self._string.write(obj)

    def flush(self) -> None:
        """
        Flush string io
        """
        self._string.flush()

    def getvalue(self) -> str:
        """
        Get string value.
        """
        return self._string.getvalue()


def youtube_main_wrapper(*args: str, show_output: bool = False) -> tuple[int, str, str]:
    """
    A wrapper to yt_dlp function with output values
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    tmp_stdout: TextIOBase
    tmp_stderr: TextIOBase

    if show_output:
        sys.stdout = tmp_stdout = _Tee()
        sys.stderr = tmp_stderr = _Tee(is_error=True)
    else:
        sys.stdout = tmp_stdout = StringIO()
        sys.stderr = tmp_stderr = StringIO()

    try:
        yt_dlp.main(list(args))
        status: Union[str, int] = 0
    except SystemExit as ex:
        if ex.code is None:
            status = 0
        else:
            status = ex.code  # pylint: disable=E0012,R0204

    sys.stdout.flush()
    sys.stderr.flush()

    if isinstance(status, str):
        status = 0
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    return status, tmp_stdout.getvalue(), tmp_stderr.getvalue()
