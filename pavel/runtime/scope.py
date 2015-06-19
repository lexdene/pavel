from collections import OrderedDict


class Scope:
    def __init__(self, defined_outer_scope=None, called_outer_scope=None, this_object=None, current_function=None):
        self.name_map = OrderedDict()
        self.defined_outer_scope = defined_outer_scope
        self.called_outer_scope = called_outer_scope
        self.this_object = this_object
        self.current_function = current_function

    def __getitem__(self, name):
        if name == 'this':
            return self.this_object

        if name in self.name_map:
            return self.name_map[name]

        if self.defined_outer_scope:
            return self.defined_outer_scope[name]

        raise KeyError(name)

    def __setitem__(self, name, value):
        self.name_map[name] = value

    def __contains__(self, name):
        if name in self.name_map:
            return True

        if self.defined_outer_scope:
            return name in self.defined_outer_scope

        return False
