from . import data_structs


class Block:
    def __init__(self):
        self.name_map = dict()

    def set_variable(self, name, value):
        self.name_map[name] = value
        return self.name_map[name]

    def get_variable(self, name):
        return self.name_map[name]

    def contains_variable(self, name):
        return name in self.name_map


class Env:
    def __init__(self):
        self.block_stack = data_structs.Stack()
        self.block_stack.push(Block())

    def current_block(self):
        return self.block_stack.top()

    def get_variable(self, name):
        for block in self.block_stack:
            if block.contains_variable(name):
                return block.get_variable(name)

        raise KeyError(name)

    def enblock(self):
        self.block_stack.push(Block())

    def deblock(self):
        return self.block_stack.pop()
