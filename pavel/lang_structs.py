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
        name = cls.OPERATOR_NAME_MAP.get(parse_tree[1], parse_tree[1])
        class_name = 'Operator' + name.title().replace('_', '')
        operator_class = globals()[class_name]
        return operator_class(parse_tree)


class OperatorAdd(LangStructBase):
    def execute(self, env, param1, param2):
        return create(param1).execute(env) + create(param2).execute(env)


class OperatorMultiply(LangStructBase):
    def execute(self, env, param1, param2):
        return create(param1).execute(env) * create(param2).execute(env)


class OperatorEqual(LangStructBase):
    def execute(self, env, param1, param2):
        return create(param1).execute(env) == create(param2).execute(env)


class OperatorLess(LangStructBase):
    def execute(self, env, param1, param2):
        return create(param1).execute(env) < create(param2).execute(env)


class OperatorMore(LangStructBase):
    def execute(self, env, param1, param2):
        return create(param1).execute(env) > create(param2).execute(env)


class OperatorAssign(LangStructBase):
    def execute(self, env, keyword_item, value_item):
        keyword = create(keyword_item)
        value = create(value_item).execute(env)

        env[keyword.name] = value

        return value


class OperatorAddAssign(LangStructBase):
    def execute(self, env, keyword_item, value_item):
        keyword = keyword_item[1]
        value = create(value_item).execute(env)

        env[keyword] = env[keyword] + value

        return value


class OperatorAttr(LangStructBase):
    def execute(self, env, object_item, attr_name):
        object_item = create(object_item).execute(env)
        attr_name = create(attr_name).name
        return object_item[attr_name]


class OperatorSetAttr(LangStructBase):
    def execute(self, env, object_item, attr_name, value):
        object_item = create(object_item).execute(env)
        attr_name = create(attr_name).name
        value = create(value).execute(value)

        object_item[attr_name] = value

        return value


class Keyword(LangStructBase):
    @property
    def name(self):
        return self._parse_tree[1]

    def execute(self, env):
        variable_name = self._parse_tree[1]
        return env[variable_name]


class IfStruct(LangStructBase):
    def execute(self, env):
        condition = self._parse_tree[1]
        then_block = self._parse_tree[2]
        else_block = self._parse_tree[3]

        condition_result = create(condition).execute(env)

        if condition_result is True:
            return create(then_block).execute(env)
        elif condition_result is False:
            if else_block:
                return create(else_block).execute(env)
        else:
            raise ValueError(
                'if condition only accept boolean, get type(%s)' % (
                    type(condition_result),
                )
            )


class WhileStruct(LangStructBase):
    def execute(self, env):
        condition = create(self._parse_tree[1])
        body = create(self._parse_tree[2])

        while condition.execute(env):
            result = body.execute(env)

        return result


class ForStruct(LangStructBase):
    def execute(self, env):
        keyword = create(self._parse_tree[1])
        expression = create(self._parse_tree[2])
        body = create(self._parse_tree[3])

        generator = expression.execute(env)

        while True:
            value, goon = generator.next()

            if goon is not True:
                break

            env[keyword.name] = value

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

        self.defined_scope = env.current_scope

        env[self.name] = self

        return self

    def call(self, env, this_object,
             params, return_type=ReturnType.return_value):
        _scope_before_call = env.current_scope

        env.current_scope = self.defined_scope
        env.enscope()

        scope = env.current_scope

        # this object
        env['this'] = this_object

        # expand params
        for formal_param, actual_param in zip(self.formal_param_list, params):
            env[formal_param[1]] = actual_param

        # execute function body
        result = create(self.body).execute(env)

        env.current_scope = _scope_before_call

        if return_type == self.ReturnType.return_value:
            return result
        elif return_type == self.ReturnType.return_name_map:
            return scope.name_map
        else:
            raise ValueError(return_type)


class FunctionCall(LangStructBase):
    def execute(self, env):
        function_object = create(self._parse_tree[1]).execute(env)

        if self._parse_tree[2]:
            # expand param value at call point
            executed_params = [
                create(param).execute(env)
                for param in self._parse_tree[2][1]
            ]
        else:
            executed_params = []

        return function_object.call(env, None, executed_params)


class MemberFunctionCall(LangStructBase):
    def execute(self, env):
        this_object = create(self._parse_tree[1]).execute(env)
        member_key = create(self._parse_tree[2])

        function_object = this_object[member_key.name]

        if self._parse_tree[3]:
            # expand params value at call point
            params = [
                create(param).execute(env)
                for param in self._parse_tree[3][1]
            ]
        else:
            params = []

        return function_object.call(env, this_object, params)


def create(parse_tree):
    struct_type_name = parse_tree[0].title().replace('_', '')
    struct_type = globals()[struct_type_name]
    return struct_type(parse_tree)
