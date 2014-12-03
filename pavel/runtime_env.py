from . import runtime_objects


class Scope:
    def __init__(self, outer_scope=None):
        self.name_map = dict()
        self.outer_scope = outer_scope

    def __getitem__(self, name):
        if name in self.name_map:
            return self.name_map[name]

        if self.outer_scope:
            return self.outer_scope[name]

        if name in runtime_objects.buildin_objects:
            return runtime_objects.buildin_objects[name]

        raise KeyError(name)

    def __setitem__(self, name, value):
        self.name_map[name] = value

    def __contains__(self, name):
        if name in self.name_map:
            return True

        if self.outer_scope:
            return name in self.outer_scope

        return False


class Env:
    def __init__(self):
        self.current_scope = Scope()

    def __getitem__(self, name):
        return self.current_scope[name]

    def __setitem__(self, name, value):
        self.current_scope[name] = value

    def __contains__(self, name):
        return name in self.current_scope

    def enscope(self):
        _scope = Scope(self.current_scope)
        self.current_scope = _scope
        return _scope

    def descope(self):
        _scope = self.current_scope.outer_scope

        if _scope is None:
            raise ValueError('no more scope to pop')

        self.current_scope = _scope
        return _scope
