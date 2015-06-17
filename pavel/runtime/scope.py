class Scope:
    def __init__(self, defined_outer_scope=None, called_outer_scope=None):
        self.name_map = dict()
        self.defined_outer_scope = defined_outer_scope
        self.called_outer_scope = called_outer_scope

    def __getitem__(self, name):
        if name in self.name_map:
            return self.name_map[name]

        if self.defined_outer_scope:
            return self.defined_outer_scope[name]

        # if name in runtime_objects.buildin_objects:
        #     return runtime_objects.buildin_objects[name]

        raise KeyError(name)

    def __setitem__(self, name, value):
        self.name_map[name] = value

    def __contains__(self, name):
        if name in self.name_map:
            return True

        if self.defined_outer_scope:
            return name in self.defined_outer_scope

        return False
