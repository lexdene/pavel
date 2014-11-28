class LangStructBase(object):
    def __init__(self, parse_tree):
        self._parse_tree = parse_tree


class MultiBlocks(LangStructBase):
    def execute(self, env):
        result = None
        for sub_tree in self._parse_tree[1]:
            result = create(sub_tree).execute(env)

        return result


class Expression(LangStructBase):
    def execute(self, env):
        if len(self._parse_tree) == 4:
            operator = create(self._parse_tree[1])
            return operator.execute(env, *self._parse_tree[2:4])


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
    }

    def __new__(cls, parse_tree):
        operator_name = cls.OPERATOR_NAME_MAP.get(parse_tree[1], parse_tree[1])
        operator_class_name = 'Operator' + operator_name.title()
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


class Keyword(LangStructBase):
    def execute(self, env):
        variable_name = self._parse_tree[1]

        block = env.current_block()
        return block.get_variable(variable_name)


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


def create(parse_tree):
    struct_type_name = parse_tree[0].title().replace('_', '')
    struct_type = globals()[struct_type_name]
    return struct_type(parse_tree)
