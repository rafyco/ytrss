import abc
from typing import TypeVar, Generic


class CoreFactoryError(Exception):
    """
    Core Factory Error
    """


RESULT = TypeVar("RESULT")
PARAMS = TypeVar("PARAMS")


class BaseFactory(Generic[PARAMS, RESULT], metaclass=abc.ABCMeta):
    """
    Base factory class
    """

    @abc.abstractmethod
    def build(self, param: PARAMS) -> RESULT:
        """
        Build defined object from parameter
        """

    def __call__(self, param: PARAMS) -> RESULT:
        return self.build(param)
