from typing import Optional


def first_line(text: Optional[str]) -> str:
    """
    Return first line of text
    """
    if text is not None:
        for line in text.split("\n"):
            if line != "":
                return line
    return ""
