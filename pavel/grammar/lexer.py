from enum import Enum
from ply import lex

from ..common.data_structs import Stack


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

        self.indents = Stack()
        self.indents.push(0)

        self.__last_token = None

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
        self.__last_token = self.lexer.token()
        return self.__last_token

    literals = r'+-*/()[],.'

    reserve_keywords = (
        'if',
        'then',
        'else',
        'for',
        'in',
        'while',
        'function',
    )

    tokens = (
        'NUMBER',
        'KEYWORD',
        'STRING',

        'ASSIGN',

        'CMP',

        'NEWLINE',
        'INDENT',
        'OUTDENT',
    ) + tuple(
        keyword.upper()
        for keyword in reserve_keywords
    )

    t_NUMBER = r'[0-9]+[a-z]?'
    t_STRING = r'"[^"]*"'
    t_CMP = r'[<>]=?|=='
    t_ASSIGN = r'[\*\/\+\-]=|=(?!=)'
    t_ignore = ' '

    def t_keyword(self, t):
        r'[a-zA-Z_][0-9a-zA-Z_]*'
        if t.value in self.reserve_keywords:
            t.type = t.value.upper()
        else:
            t.type = 'KEYWORD'

        return t

    def t_newline(self, t):
        r'\n[ ]*'

        if len(t.lexer.lexdata) > t.lexer.lexpos:
            next_char = t.lexer.lexdata[t.lexer.lexpos]
            if next_char == '\n':
                t.lexer.lineno += 1
                # do nothing with empty line
                return

        # remove '\n'
        width = len(t.value) - 1

        last_indent = self.indents.top()

        if width > last_indent:
            self.indents.push(width)
            t.type = 'INDENT'
            return t
        elif width < last_indent:
            # 这种记录last_token的做法实在是很恶心
            # 但我暂时也没找到更好的办法解决这个问题
            if self.__last_token.type == 'NEWLINE':
                self.indents.pop()

                t.lexer.skip(-len(t.value))

                t.type = 'OUTDENT'
                return t
            else:
                t.lexer.skip(-len(t.value))
                t.lexer.lineno += 1

                t.type = 'NEWLINE'
                return t
        else:
            t.lexer.lineno += 1

            t.type = 'NEWLINE'
            return t

    def t_comment(self, t):
        '\#[^\n]*(?=\n)'
        pass

    def t_error(self, t):
        raise ValueError(t)
