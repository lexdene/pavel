from collections import OrderedDict


class PvlObject:
    def __init__(self, cls, data):
        assert cls is not None
        assert isinstance(data, dict)

        self.cls = cls
        self.data = data

    def get_attr(self, scope, name):
        return self.cls.get_attr(scope, self, name)

    def set_attr(self, scope, name, value):
        return self.cls.set_attr(scope, self, name, value)

    def call(self, scope, this_object, params, **kwargs):
        return self.cls.call(scope, this_object, params, self, **kwargs)


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

    def get_attr(self, scope, instance, name, delegators_enable=True):
        if delegators_enable and self.__delegators and 'get' in self.__delegators:
            return self.__delegators['get'].call(
                scope,
                _ThisObject(instance, self),
                [name],
            )
        elif name in self.__attrs:
            return self.__attrs[name]
        else:
            for p in self.__parents:
                if p.has_attr(name):
                    return p.get_attr(name, instance)

        raise AttributeError(
            '%s object has no attribute %s' % (
                repr(self.__name),
                repr(name)
            )
        )

    def set_attr(self, scope, instance, name, value):
        if self.__delegators and 'set' in self.__delegators:
            return self.__delegators['set'].call(
                scope,
                _ThisObject(instance, self),
                [name, value],
            )

    def call(self, scope, this_object, params, instance, **kwargs):
        if self.__delegators and 'call' in self.__delegators:
            return self.__delegators['call'].call(
                scope,
                _ThisObject(instance, self),
                params,
                **kwargs
            )
        else:
            raise AttributeError('no call method')

    def get_super(self):
        return self.__parents[0]


class _ThisObject(PvlObject):
    def __init__(self, instance, chain_point, in_delegator=False):
        self.instance = instance
        self.chain_point = chain_point
        self.in_delegator = in_delegator

        super(_ThisObject, self).__init__(
            self.chain_point,
            self.instance.data
        )

    def get_attr(self, scope, name):
        return self.chain_point.get_attr(
            scope,
            self.instance,
            name,
            self.in_delegator
        )

    def __repr__(self):
        return '<%s.%s object (%s, %s, %s)>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.instance,
            self.chain_point,
            self.in_delegator
        )
