import re
from typing import Optional

ERROR_MARK = "ERROR:"
MAX_ERROR_TYPE_LENGTH = 200


def first_line(text: Optional[str]) -> str:
    """
    Return first line of text
    """
    if text is not None:
        for line in text.split("\n"):
            if line != "":
                return line
    return ""


def error_type(cause: str) -> str:
    """
    Return text that is the same for one kind of error, whatever movie it comes from

    The mark of error is looked for inside of the line too, because errors from creating a movie put
    the output of yt_dlp after their own text, and that text has the url of the movie.
    """
    lines = [line for line in cause.splitlines() if ERROR_MARK in line]
    if lines:
        message = lines[-1].split(ERROR_MARK, 1)[1]
    else:
        message = first_line(cause)
    message = re.sub(r"^\[[^\]]+\] \S+?: ", "", message.strip())
    return re.sub(r"\d+", "#", message)[:MAX_ERROR_TYPE_LENGTH]
