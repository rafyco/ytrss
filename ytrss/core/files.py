import os
from contextlib import contextmanager

from typing import ContextManager


@contextmanager
def cwd(cwd_path: str) -> ContextManager:
    """
    Change work directory

    This context manager change work directory where the script was executed. It also back to
    previous directory, at the end of script.

    TODO: Check how to make warn in documentation
    .. warn:
        After end of 'with' structure, the work directory will be back to previous state, even
        if it's change according the structure.
    """
    old_path = os.getcwd()
    os.chdir(cwd_path)
    yield
    os.chdir(old_path)
