from collections import OrderedDict


class Env:
    def __init__(self):
        self.this_object = None
        self.name_map = OrderedDict()
        self.current_scope = None

        # save the original arguments
        self.arguments = None

        # called outer env
        self.called_env = None

    def set_variable(self, name, value):
        self.name_map[name] = value

    def get_variable(self, name):
        return self.name_map[name]


class Block:
    def eval(self, env):
        pass


class Scope:
    def eval(self, env):
        former_scope = env.current_scope
        env.current_scope = self

        result = None

        for block in self.blocks:
            result = block.eval(env)

        env.current_scope = former_scope
        return result


def _find_by_name(arguments, name):
    pass


class Function:
    def __init__(self):
        self.name = None
        self.defined_arguments = []
        self.scope = None

    def call(self, env, this_object, arguments):
        new_env = Env()
        new_env.this_object = this_object
        new_env.called_env = env

        for index, def_arg in enumerate(self.defined_arguments):
            name, default_expression = def_arg

            found, found_value = _find_by_name(arguments, name)
            if found:
                value = found_value
            elif index >= len(arguments):
                value = default_expression.eval(new_env)
            else:
                arg_name, arg_value = arguments[index]
                if arg_name is None:
                    value = arg_value
                else:
                    value = default_expression.eval(new_env)

            new_env.set_variable(name, value)

        return self.scope.eval(new_env)
