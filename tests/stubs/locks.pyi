from types import TracebackType
from typing import ContextManager, AnyStr, Callable, Optional, Type


class Mutex(ContextManager[None]):

    def __init__(self, path: AnyStr, timeout: Optional[float] = None, callback: Optional[Callable[[], None]] = None): ...

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], traceback: Optional[TracebackType]
    ) -> Optional[bool]: ...
