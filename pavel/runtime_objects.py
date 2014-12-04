class _ObjectConstructor:
    def call(self, env, this_object, argument_list):
        block = argument_list[0]

        data = argument_list[0].call(
            env,
            this_object,
            [],
            return_type=block.ReturnType.return_name_map
        )

        return _Object(data)


class _Object:
    def __init__(self, data=None):
        if data:
            self.__data = data

    def __getitem__(self, attr_name):
        return self.__data[attr_name]

    def __setitem__(self, attr_name, value):
        self.__data[attr_name] = value
        return value


class _RangeWrapper:
    def call(self, env, this_object, argv):
        return _RangeGenerator(argv[0])


class _RangeGenerator:
    def __init__(self, n):
        self.__n = n
        self.__i = -1

    def next(self):
        self.__i += 1

        goon = self.__i < self.__n

        return self.__i, goon


buildin_objects = dict(
    lang=dict(
        object=_ObjectConstructor(),
        range=_RangeWrapper(),
    )
)
