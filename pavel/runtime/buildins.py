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
    key = params[0]
    return this_object.instance.data[key]


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

    # delegated_class = object.PvlClass(
    #     name=None,
    #     attrs=(),
    #     delegators=(
    #         (key, value)
    #         for key, value in data.items()
    #     ),
    #     parents=(object_class,),
    # )

    # return delegator
    return object.PvlObject(
        cls=delegator_class,
        data=dict(
            delegators=(
                (key, value)
                for key, value in data.items()
            ),
        )
    )


@native_function
def delegator_call(scope, this_object, params, **kwargs):
    inner_object = params[0]

    delegated_class = object.PvlClass(
        name=None,
        attrs=(),
        delegators=this_object.instance.data['delegators'],
        parents=(inner_object.cls,),
    )

    return object.PvlObject(
        cls=delegated_class,
        data=inner_object.data,
    )


delegator_class = object.PvlClass(
    name="Delegator",
    attrs=(),
    delegators=(
        ('call', delegator_call),
    ),
    parents=(),
)


@native_function
def pvl_super(scope, this_object, params, **kwargs):
    if scope.this_object.in_delegator:
        result = object._ThisObject(
            scope.this_object.instance,
            scope.this_object.chain_point,
            False,
        )
    else:
        result = object._ThisObject(
            scope.this_object.instance,
            scope.this_object.chain_point.get_super(),
            True,
        )

    return result


buildins = dict(
    lang=dict(
        object=object_constructor,
        range=range,
        delegator=delegator_constructor,
        super=pvl_super,
    )
)
