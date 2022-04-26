import re
import time
from datetime import datetime
from email import utils

from typing import Optional


def format_desc(text: Optional[str]) -> str:
    """
    Format description.

    This function replace ulr and newline chars by following html code.
    It is using in rss file to format description in rss reader.
    """
    if text is None:
        return ""
    result = text
    result = re.sub(r"[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}",
                    r"<a href='mailto:\g<0>'>\g<0></a>",
                    result)
    result = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|i"
                    "(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                    r"<a href='\g<0>'>\g<0></a>",
                    result)
    result = re.sub(r"\/redirect(?:[a-zA-Z0-9$-_@.&!*\(\)]*)(?:q=(?P<url>[A-Za-z0-9%.]+))+"
                    "(?:[a-zA-Z0-9$-_@.&!*,]*)",
                    r"<a href='\g<url>'>\g<url></a>",
                    result)
    result = re.sub(r"\/(?:redirect|watch)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
                    "(?:%[0-9a-zA-Z][0-9a-zA-Z]))+",
                    r"<a href='https://youtube.com\g<0>'>\g<0></a>",
                    result)
    result = result.replace("\n", "<br />\n")
    result = result.replace("%3A", ":")
    result = result.replace("%2F", "/")
    return result


def format_str(text: Optional[str]) -> str:
    """
    Format some strings.

    This function replacing invalid chars in xml file.
    ex. RSS doesn't accept C{&} char, so it should be replaced to C{&amp;}
    """
    return text.replace("&", "&amp;") if text is not None else ""


def format_date(date: Optional[datetime]) -> str:
    """
    Convert datetime to string
    """
    print_date: datetime = date if date is not None else datetime.now()
    return utils.formatdate(time.mktime(print_date.timetuple()))
