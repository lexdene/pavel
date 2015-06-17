from enum import Enum

from . import object

class FunctionReturnType(Enum):
    RETURN_VALUE = 1
    RETURN_NAME_MAP = 2
    RETURN_SCOPE = 3
    RETURN_LIST_BY_LINES = 4


class PvlFunction(object.PvlObject):
    def call(self):
        pass


class NativeFunction(PvlFunction):
    '''
        native means function written in Python
    '''
    def __init__(self, func):
        self.__func = func

    def call(self, *argv, **kwargs):
        return self.__func(*argv, **kwargs)


# for decorator
# it is said that the name of decorator should be in lower letters
native_function = NativeFunction
