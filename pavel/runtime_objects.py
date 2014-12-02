class _ObjectConstructor:
    def call(self, env, argument_list):
        block = argument_list[0]

        data = argument_list[0].call(
            env,
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


buildin_objects = dict(
    lang=dict(
        object=_ObjectConstructor()
    )
)
