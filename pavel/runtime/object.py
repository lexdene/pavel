from collections import OrderedDict


class PvlObject:
    def __init__(self, cls, data):
        self.cls = cls
        self.data = data

    def get_attr(self, scope, name):
        return self.cls.get_attr(scope, self, name)

    def set_attr(self, scope, name, value):
        return self.cls.set_attr(scope, self, name, value)

    def call(self, scope, this_object, params, **kwargs):
        pass


class PvlClass:
    def __init__(self, name, attrs, delegators, parents):
        # name maybe none or a string
        # TODO: generate a random name if name is None
        self.__name = name

        # attrs should be a 2-level tuple
        self.__attrs = OrderedDict(attrs)

        # delegator maybe none or a 2-level tuple
        if delegators:
            self.__delegators = OrderedDict(delegators)
        else:
            self.__delegators = None

        # parents should be a tuple
        self.__parents = parents

    def get_attr(self, scope, obj, name):
        if self.__delegators and 'get' in self.__delegators:
            return self.__delegators['get'].call(
                scope,
                _ThisObject(obj, self),
                [name],
            )
        elif name in self.__attrs:
            return self.__attrs[name]
        else:
            for p in self.__parents:
                if p.has_attr(name):
                    return p.get_attr(name, obj)

        raise AttributeError(
            '%s object has no attribute %s' % (
                repr(self.__name),
                repr(name)
            )
        )

    def set_attr(self, scope, obj, name, value):
        if self.__delegators and 'set' in self.__delegators:
            return self.__delegators['set'].call(
                scope,
                _ThisObject(obj, self),
                [name, value],
            )


class _ThisObject:
    def __init__(self, obj, chain_point, in_delegator=False):
        self.obj = obj
        self.chain_point = chain_point
        self.in_delegator = in_delegator
