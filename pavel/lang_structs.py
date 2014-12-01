from enum import Enum


class LangStructBase(object):
    def __init__(self, parse_tree):
        self._parse_tree = parse_tree


class MultiLines(LangStructBase):
    def execute(self, env):
        result = None
        for sub_tree in self._parse_tree[1]:
            result = create(sub_tree).execute(env)

        return result


class Expression(LangStructBase):
    def execute(self, env):
        operator = create(self._parse_tree[1])
        return operator.execute(env, *self._parse_tree[2:])


class Number(LangStructBase):
    def execute(self, env):
        return int(self._parse_tree[1])


class Operator(LangStructBase):
    OPERATOR_NAME_MAP = {
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide',
        '==': 'equal',
        '<': 'less',
        '>': 'more',
        '=': 'assign',
        '+=': 'add_assign',
        '.': 'attr',
    }

    def __new__(cls, parse_tree):
        operator_name = cls.OPERATOR_NAME_MAP.get(parse_tree[1], parse_tree[1])
        operator_class_name = 'Operator' + operator_name.title().replace('_', '')
        operator_class = globals()[operator_class_name]
        return operator_class(parse_tree)


class OperatorAdd(LangStructBase):
    def execute(self, env, arg1, arg2):
        return create(arg1).execute(env) + create(arg2).execute(env)


class OperatorMultiply(LangStructBase):
    def execute(self, env, arg1, arg2):
        return create(arg1).execute(env) * create(arg2).execute(env)


class OperatorEqual(LangStructBase):
    def execute(self, env, arg1, arg2):
        return create(arg1).execute(env) == create(arg2).execute(env)


class OperatorLess(LangStructBase):
    def execute(self, env, arg1, arg2):
        return create(arg1).execute(env) < create(arg2).execute(env)


class OperatorMore(LangStructBase):
    def execute(self, env, arg1, arg2):
        return create(arg1).execute(env) > create(arg2).execute(env)


class OperatorAssign(LangStructBase):
    def execute(self, env, keyword_item, value_item):
        value = create(value_item).execute(env)

        block = env.current_block()
        block.set_variable(keyword_item[1], value)

        return value


class OperatorAddAssign(LangStructBase):
    def execute(self, env, keyword_item, value_item):
        keyword = keyword_item[1]
        value = create(value_item).execute(env)

        block = env.current_block()
        block.set_variable(
            keyword,
            block.get_variable(keyword) + value
        )

        return value


class OperatorAttr(LangStructBase):
    def execute(self, env, object_item, attr_name):
        object_item = create(object_item).execute(env)
        attr_name = create(attr_name).name
        return object_item.get_attr(attr_name)


class OperatorSetAttr(LangStructBase):
    def execute(self, env, object_item, attr_name, value):
        object_item = create(object_item).execute(env)
        attr_name = create(attr_name).name
        value = create(value).execute(value)

        return object_item.set_attr(attr_name, value)


class Keyword(LangStructBase):
    @property
    def name(self):
        return self._parse_tree[1]

    def execute(self, env):
        variable_name = self._parse_tree[1]

        return env.get_variable(variable_name)


class IfStruct(LangStructBase):
    def execute(self, env):
        condition = self._parse_tree[1]
        then_block = self._parse_tree[2]
        else_block = self._parse_tree[3]

        if create(condition).execute(env):
            return create(then_block).execute(env)
        else:
            if else_block:
                return create(else_block).execute(env)


class WhileStruct(LangStructBase):
    def execute(self, env):
        condition = create(self._parse_tree[1])
        body = create(self._parse_tree[2])

        while condition.execute(env):
            result = body.execute(env)

        return result


class FunctionStruct(LangStructBase):
    class ReturnType(Enum):
        return_value = 1
        return_name_map = 2
        return_list_by_lines = 3

    def execute(self, env):
        if self._parse_tree[1]:
            self.name = self._parse_tree[1][1]
        else:
            self.name = None

        if self._parse_tree[2]:
            self.formal_param_list = self._parse_tree[2][1]
        else:
            self.formal_param_list = []

        self.body = self._parse_tree[3]

        block = env.current_block()
        block.set_variable(
            self.name,
            self
        )

        return self

    def call(self, env, argument_list, return_type=ReturnType.return_value):
        env.enblock()

        # expand params
        block = env.current_block()
        for formal_param, actual_param in zip(self.formal_param_list, argument_list):
            block.set_variable(formal_param[1], actual_param)

        # execute function body
        result = create(self.body).execute(env)

        env.deblock()

        if return_type == self.ReturnType.return_value:
            return result
        elif return_type == self.ReturnType.return_name_map:
            return block.name_map
        else:
            raise ValueError(return_type)


class FunctionCall(LangStructBase):
    def execute(self, env):
        function_object = create(self._parse_tree[1]).execute(env)

        # expand argument value at call point
        executed_arguments = [
            create(arg).execute(env)
            for arg in self._parse_tree[2][1]
        ]

        return function_object.call(env, executed_arguments)


def create(parse_tree):
    struct_type_name = parse_tree[0].title().replace('_', '')
    struct_type = globals()[struct_type_name]
    return struct_type(parse_tree)
