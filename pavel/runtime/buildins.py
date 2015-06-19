from . import object
from .function import FunctionReturnType, native_function


@native_function
def object_constructor(scope, this_object, params):
    data = params[0].call(
        scope,
        this_object,
        [],
        return_type=FunctionReturnType.RETURN_NAME_MAP
    )

    return object.PvlObject(
        cls=object_class,
        data=data
    )


@native_function
def object_get(scope, this_object, params, **kwargs):
    return this_object.instance.data[params[0]]


@native_function
def object_set(scope, this_object, params, **kwargs):
    key = params[0]
    value = params[1]
    this_object.instance.data[key] = value
    return value


object_class = object.PvlClass(
    name="Object",
    attrs=(),
    delegators=(
        ('get', object_get),
        ('set', object_set),
    ),
    parents=()
)

# class _Object(PavelObject):
#     def __init__(self, data=None):
#         if data:
#             self.__data = data

#     def get_attr(self, scope, attr_name):
#         return self.__data[attr_name]

#     def __setitem__(self, attr_name, value):
#         self.__data[attr_name] = value
#         return value


@native_function
def range(scope, this_object, params):
    return _RangeGenerator(params[0])


class _RangeGenerator:
    def __init__(self, n):
        self.__n = n
        self.__i = -1

    def next(self):
        self.__i += 1

        goon = self.__i < self.__n

        return self.__i, goon


@native_function
def delegator_constructor(scope, this_object, params):
    block = params[0]

    data = params[0].call(
        scope,
        this_object,
        [],
        return_type=FunctionReturnType.RETURN_NAME_MAP
    )

    # delegator = _Delegator(scope.name_map)
    # scope.defined_object = delegator

    delegated_class = object.PvlClass(
        name=None,
        attrs=(),
        delegators=(
            (key, value)
            for key, value in data.items()
        ),
        parents=(),
    )

    # return delegator
    return object.PvlObject(
        cls=delegator_class,
        data=dict(
            delegated_class=delegated_class,
            original_data=data,
        )
    )


@native_function
def delegator_call(scope, this_object, params, **kwargs):
    print('delegator call:')
    print(this_object, params)
    print(this_object.instance.data)

    data = params[0].call(
        scope,
        this_object,
        [],
        return_type=FunctionReturnType.RETURN_NAME_MAP
    )

    return object.PvlObject(
        cls=this_object.instance.data['delegated_class'],
        data=data
    )


delegator_class = object.PvlClass(
    name="Delegator",
    attrs=(),
    delegators=(
        ('call', delegator_call),
    ),
    parents=(),
)


# class _PavelFunctionWrapper(_PavelObject):
#     def __init__(self, func):
#         self.__func = func

#     def call(
#         self,
#         scope,
#         this_object,
#         params,
#         return_type=FunctionReturnType.RETURN_VALUE
#     ):
#         assert return_type == FunctionReturnType.RETURN_VALUE

#         return self.__func(scope, this_object, params)


# class _PavelFunction(_PavelObject):
#     def __init__(self, func):
#         self.__func = func

#     def __repr__(self):
#         return 'PavelFunction: %s' % repr(self.__func)

#     @_PavelFunctionWrapper
#     def args_call(scope, this_object, params):
#         obj = params[0].get_obj()
#         name = params[1]
#         return obj.get_attr(scope, name)


# class _DefaultDelegator(_PavelObject):
#     @_PavelFunction
#     def get(self, scope, attr_name):
#         pass


# class _Delegator:
#     def __init__(self, data):
#         self.__data = data

#     def call(self, scope, this_object, params):
#         return _DelegatedObject(scope, self.__data, params[0])

#     def get_super(self):
#         return _DefaultDelegator()


# class _DelegatedObject(PavelObject):
#     def __init__(self, scope, delegator, obj):
#         self.__delegator = delegator
#         self.__obj = obj

#     def get_attr(self, scope, name):
#         return self.__delegator['get'].call(
#             scope,
#             self,
#             [name],
#         )

#     def get_obj(self):
#         return self.__obj


# class _SuperWrapper:
#     def call(self, scope, this_object, params):
#         result = None
#         return scope.current_function.defined_scope.defined_object.get_super()


buildins = dict(
    lang=dict(
        object=object_constructor,
        range=range,
        delegator=delegator_constructor,
        # super=_SuperWrapper(),
    )
)
