def assert_not_empty(func):
    def inner_wrapper(self):
        assert not self.is_empty()
        return func(self)

    return inner_wrapper


class Stack:
    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def __str__(self):
        return str(self.__data)

    def __iter__(self):
        return reversed(self.__data)

    def is_empty(self):
        return len(self) == 0

    @assert_not_empty
    def top(self):
        return self.__data[-1]

    @assert_not_empty
    def pop(self):
        return self.__data.pop()

    def push(self, value):
        return self.__data.append(value)
