class object:
    @classmethod
    def call(cls, env, argument_list):
        return cls(env, argument_list[0])

    def __init__(self, env, block):
        self.env = env
        self.__data = block.call(
            env,
            [],
            return_type=block.ReturnType.return_name_map
        )

    def get_attr(self, attr_name):
        return self.__data[attr_name]

    def set_attr(self, attr_name, value):
        self.__data[attr_name] = value
        return value
