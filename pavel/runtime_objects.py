from enum import Enum


class FunctionReturnType(Enum):
    RETURN_VALUE = 1
    RETURN_NAME_MAP = 2
    RETURN_SCOPE = 3
    RETURN_LIST_BY_LINES = 4


class _ObjectConstructor:
    def call(self, env, this_object, params):
        block = params[0]

        data = params[0].call(
            env,
            this_object,
            [],
            return_type=FunctionReturnType.RETURN_NAME_MAP
        )

        return _Object(data)


class _Object:
    def __init__(self, data=None):
        if data:
            self.__data = data

    def get_attr(self, env, attr_name):
        return self.__data[attr_name]

    def __setitem__(self, attr_name, value):
        self.__data[attr_name] = value
        return value


class _DictWrapper:
    def __init__(self, **kwargs):
        self.__data = kwargs

    def get_attr(self, env, attr_name):
        return self.__data[attr_name]


class _RangeWrapper:
    def call(self, env, this_object, params):
        return _RangeGenerator(params[0])


class _RangeGenerator:
    def __init__(self, n):
        self.__n = n
        self.__i = -1

    def next(self):
        self.__i += 1

        goon = self.__i < self.__n

        return self.__i, goon


class _DelegatorWrapper:
    def call(self, env, this_object, params):
        block = params[0]

        scope = params[0].call(
            env,
            this_object,
            [],
            return_type=FunctionReturnType.RETURN_SCOPE
        )

        delegator = _Delegator(scope.name_map)
        scope.defined_object = delegator

        return delegator


class _PavelObject:
    def get_attr(self, env, attr_name):
        return getattr(self, attr_name)


class _PavelFunctionWrapper(_PavelObject):
    def __init__(self, func):
        self.__func = func

    def call(
        self,
        env,
        this_object,
        params,
        return_type=FunctionReturnType.RETURN_VALUE
    ):
        assert return_type == FunctionReturnType.RETURN_VALUE

        return self.__func(env, this_object, params)


class _PavelFunction(_PavelObject):
    def __init__(self, func):
        self.__func = func

    def __repr__(self):
        return 'PavelFunction: %s' % repr(self.__func)

    @_PavelFunctionWrapper
    def args_call(env, this_object, params):
        obj = params[0].get_obj()
        name = params[1]
        return obj.get_attr(env, name)


class _DefaultDelegator(_PavelObject):
    @_PavelFunction
    def get(self, env, attr_name):
        pass


class _Delegator:
    def __init__(self, data):
        self.__data = data

    def call(self, env, this_object, params):
        return _DelegatedObject(env, self.__data, params[0])

    def get_super(self):
        return _DefaultDelegator()


class _DelegatedObject:
    def __init__(self, env, delegator, obj):
        self.__delegator = delegator
        self.__obj = obj

    def get_attr(self, env, name):
        return self.__delegator['get'].call(
            env,
            self,
            [name],
        )

    def get_obj(self):
        return self.__obj


class _SuperWrapper:
    def call(self, env, this_object, params):
        result = None
        return env.current_function.defined_scope.defined_object.get_super()


buildin_objects = dict(
    lang=_DictWrapper(
        object=_ObjectConstructor(),
        range=_RangeWrapper(),
        delegator=_DelegatorWrapper(),
        super=_SuperWrapper(),
    )
)
