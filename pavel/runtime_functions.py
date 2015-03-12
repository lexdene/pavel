from . import runtime_objects


def get_attr(obj, attr, env):
    if isinstance(obj, runtime_objects.PavelObject):
        return obj.get_attr(env, attr)
    if hasattr(obj, '__getitem__'):
        return obj[attr]
    else:
        return getattr(obj, attr)
