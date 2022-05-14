from typing import ContextManager, AnyStr, Callable, Optional


class Mutex(ContextManager[None]):

    def __init__(self, path: AnyStr, timeout: Optional[float] = None, callback: Optional[Callable[[], None]] = None): ...
