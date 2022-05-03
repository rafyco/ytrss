import abc
from typing import TypeVar, Generic, Sequence, Callable, Optional


RESULT = TypeVar("RESULT")
PARAMS = TypeVar("PARAMS")


class FactoryError(Exception):
    """ Factory error

    An exception raised when the factory cannot create an object from arguments.
    """


class BaseFactory(Generic[PARAMS, RESULT], metaclass=abc.ABCMeta):
    """ A base of factory """

    @property
    @abc.abstractmethod
    def plugins(self) -> Sequence[Callable[[PARAMS], Optional[RESULT]]]:
        """ A list of function that try to produce a file """

    def build(self, param: PARAMS) -> RESULT:
        for plugin in self.plugins:
            try:
                result = plugin(param)
                if result is not None:
                    return result
            except Exception:  # pylint: disable=W0703
                pass
        raise FactoryError(
            "Cannot create object by (%s) from %s",
            type(self),
            param
        )

    def __call__(self, param: PARAMS) -> RESULT:
        return self.build(param)
