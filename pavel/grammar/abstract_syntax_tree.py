from ..runtime.scope import Scope
from ..runtime.function import FunctionReturnType
from ..runtime import utils as runtime_utils

class AbstractSyntaxNode:
    def __init__(self, parse_tree):
        self._node_name = parse_tree[0]
        self._data = parse_tree[1]

    def __getattr__(self, name):
        return self._data[name]


class MultiLines(AbstractSyntaxNode):
    def execute(self, scope):
        result = None
        for sub_tree in self.lines:
            result = create(sub_tree).execute(scope)

        return result


class Expression(AbstractSyntaxNode):
    def execute(self, scope):
        operator = create(self.operator)
        return operator.execute(scope, self.args)


class Number(AbstractSyntaxNode):
    def execute(self, scope):
        return int(self._data)


class String(AbstractSyntaxNode):
    def execute(self, scope):
        return self._data[1:-1]


class Operator(AbstractSyntaxNode):
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
        '[]': 'item',
    }

    def __new__(cls, parse_tree):
        name = cls.OPERATOR_NAME_MAP.get(parse_tree[1], parse_tree[1])
        class_name = 'Operator' + name.title().replace('_', '')
        operator_class = globals()[class_name]
        return operator_class(parse_tree)


class OperatorAdd(AbstractSyntaxNode):
    def execute(self, scope, args):
        return create(args[0]).execute(scope) + create(args[1]).execute(scope)


class OperatorMultiply(AbstractSyntaxNode):
    def execute(self, scope, args):
        return create(args[0]).execute(scope) * create(args[1]).execute(scope)


class OperatorEqual(AbstractSyntaxNode):
    def execute(self, scope, args):
        return create(args[0]).execute(scope) == create(args[1]).execute(scope)


class OperatorLess(AbstractSyntaxNode):
    def execute(self, scope, args):
        return create(args[0]).execute(scope) < create(args[1]).execute(scope)


class OperatorMore(AbstractSyntaxNode):
    def execute(self, scope, args):
        return create(args[0]).execute(scope) > create(args[1]).execute(scope)


class OperatorAssign(AbstractSyntaxNode):
    def execute(self, scope, args):
        keyword = create(args[0])
        value = create(args[1]).execute(scope)

        scope[keyword.name] = value

        return value


class OperatorAddAssign(AbstractSyntaxNode):
    def execute(self, scope, args):
        keyword = create(args[0])
        value = create(args[1]).execute(scope)

        scope[keyword.name] = scope[keyword.name] + value

        return value


class OperatorAttr(AbstractSyntaxNode):
    def execute(self, scope, args):
        object_item = create(args[0]).execute(scope)
        attr_name = create(args[1]).name
        return runtime_utils.get_attr(scope, object_item, attr_name)


class OperatorSetAttr(AbstractSyntaxNode):
    def execute(self, scope, args):
        object_item = create(args[0]).execute(scope)
        attr_name = create(args[1]).name
        value = create(args[2]).execute(scope)

        runtime_utils.set_attr(scope, object_item, attr_name, value)

        return value


class OperatorItem(AbstractSyntaxNode):
    def execute(self, scope, args):
        print('operator item:', args)
        object_item = create(args[0]).execute(scope)
        attr_name = create(args[1]).execute(scope)
        return runtime_utils.get_attr(scope, object_item, attr_name)


class Keyword(AbstractSyntaxNode):
    def execute(self, scope):
        variable_name = self.name
        return scope[variable_name]


class IfStruct(AbstractSyntaxNode):
    def execute(self, scope):
        condition_result = create(self.condition).execute(scope)

        if condition_result is True:
            return create(self.then_block).execute(scope)
        elif condition_result is False:
            if self.else_block:
                return create(self.else_block).execute(scope)
        else:
            raise ValueError(
                'if condition only accept boolean, get type(%s)' % (
                    type(condition_result),
                )
            )


class WhileStruct(AbstractSyntaxNode):
    def execute(self, scope):
        condition = create(self.condition)

        # body is an anonymous function
        # get its body and run in current scope
        body = create(create(self.body).body)

        while condition.execute(scope):
            result = body.execute(scope)

        return result


class ForStruct(AbstractSyntaxNode):
    def execute(self, scope):
        keyword = create(self.keyword)
        expression = create(self.expression)
        body = create(self.body)

        generator = expression.execute(scope)

        while True:
            value, goon = generator.next()

            if goon is not True:
                break

            scope[keyword.name] = value

            result = body.execute(scope)

        return result


class FunctionStruct(AbstractSyntaxNode):
    def execute(self, scope):
        if self.name:
            name = create(self.name).name
        else:
            name = None
        params = self.params
        body = self.body
        self.defined_scope = scope

        if name:
            scope[name] = self

        return self

    def call(self, scope, this_object, params, **kwargs):
        # _scope_before_call = scope

        scope_in_call = Scope(
            called_outer_scope=scope,
            defined_outer_scope=self.defined_scope,
            this_object=this_object,
            current_function=self
        )
        # scope.current_scope = self.defined_scope
        # scope = scope.enscope()

        # this object
        # scope_in_call.this_object = this_object
        # scope_in_call.current_function = self

        # expand params
        for formal_param, actual_param in zip(self.params, params):
            formal_param = create(formal_param)
            scope_in_call[formal_param.name] = actual_param

        # execute function body
        result = create(self.body).execute(scope_in_call)

        return_type = kwargs.get(
            'return_type',
            FunctionReturnType.RETURN_VALUE
        )

        if return_type == FunctionReturnType.RETURN_VALUE:
            return result
        elif return_type == FunctionReturnType.RETURN_NAME_MAP:
            return scope_in_call.name_map
        elif return_type == FunctionReturnType.RETURN_SCOPE:
            return scope_in_call
        else:
            raise ValueError(return_type)


class FunctionCall(AbstractSyntaxNode):
    def execute(self, scope):
        function_object = create(self.function).execute(scope)

        # expand param value at call point
        executed_params = [
            create(param).execute(scope)
            for param in self.params
        ]

        return function_object.call(scope, None, executed_params)


class MemberFunctionCall(AbstractSyntaxNode):
    def execute(self, scope):
        this_object = create(self.this_object).execute(scope)
        member_key = create(self.name)

        function_object = runtime_utils.get_attr(scope, this_object, member_key.name)

        # expand params value at call point
        params = [
            create(param).execute(scope)
            for param in self.params
        ]

        return function_object.call(scope, this_object, params)


def create(parse_tree):
    struct_type_name = parse_tree[0].title().replace('_', '')
    struct_type = globals()[struct_type_name]
    return struct_type(parse_tree)
