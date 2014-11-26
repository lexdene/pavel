from enum import Enum
from ply import lex


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, source):
        self.lexer.input(source)

    def __iter__(self):
        while True:
            token = self.token()
            if token:
                yield token
            else:
                break

    def token(self):
        return self.lexer.token()

    literals = '+-*/='
    tokens = (
        'NUMBER',
        'KEYWORD',
    )

    t_NUMBER = r'[0-9]+[a-z]?'
    t_KEYWORD = r'[a-zA-Z_][0-9a-zA-Z_]*'
    t_ignore = ' \n'

    def t_error(self, t):
        raise ValueError(t)
