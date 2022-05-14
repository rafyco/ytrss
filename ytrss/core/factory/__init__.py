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
        """ A list of functions that try to produce an object """

    def build(self, param: PARAMS) -> RESULT:
        """
        Build an object

        Look for all plugins and try to build a new one object. It there are a problem with object
        the FactoryError will be returned.
        """
        for plugin in self.plugins:
            try:
                result = plugin(param)
                if result is not None:
                    return result
            except Exception:  # pylint: disable=W0703
                pass
        raise FactoryError(f"Cannot create object by ({type(self)}) from {param}")

    def __call__(self, param: PARAMS) -> RESULT:
        return self.build(param)
