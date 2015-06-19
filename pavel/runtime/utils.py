from . import object


def get_attr(scope, obj, attr):
    print('utils get attr:')
    print(obj, attr)
    if isinstance(obj, object.PvlObject):
        return obj.get_attr(scope, attr)
    elif hasattr(obj, '__getitem__'):
        return obj[attr]
    else:
        return getattr(obj, attr)


def set_attr(scope, obj, attr, value):
    if isinstance(obj, object.PvlObject):
        return obj.set_attr(scope, attr, value)
    elif hasattr(obj, '__setitem__'):
        obj[attr] = value
        return value
    else:
        return setattr(obj, attr, value)
