import abc
from typing import TypeVar, Generic


class CoreFactoryError(Exception):
    pass


RESULT = TypeVar("RESULT")
PARAMS = TypeVar("PARAMS")


class BaseFactory(Generic[PARAMS, RESULT], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build(self, param: PARAMS) -> RESULT:
        pass

    def __call__(self, param: PARAMS) -> RESULT:
        return self.build(param)
