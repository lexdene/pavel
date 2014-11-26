from ply import yacc

from . import lexer


class Parser:
    def _create_lexer(self):
        return lexer.Lexer()

    def parse(self, source):
        # self._debug_parse_tokens(source)

        parser = yacc.yacc(module=self)
        return parser.parse(
            source,
            lexer=self._create_lexer()
        )

    def _debug_parse_tokens(self, source):
        _lexer = self._create_lexer()
        print(' ==== debug begin ==== ')

        print(source)
        print(repr(source))

        _lexer.input(source)
        for tok in _lexer:
            print(
                '%15s, %40s %3d %3d' % (
                    tok.type, repr(tok.value), tok.lineno, tok.lexpos
                )
            )

        print(' ==== debug end ==== ')
        print('')

    tokens = lexer.Lexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def p_first_rule(self, p):
        '''
            first_rule : multi_blocks
        '''
        p[0] = p[1]

    def p_error(self, p):
        raise ValueError(p)

    def p_multi_blocks(self, p):
        '''
            multi_blocks : empty
                         | block
                         | multi_blocks block
        '''
        if len(p) == 2:
            if p[1] is None:
                p[0] = (
                    'multi_blocks',
                    []
                )
            else:
                p[0] = (
                    'multi_blocks',
                    [p[1]]
                )
        elif len(p) == 3:
            block_list = p[1][1]
            block_list.append(p[2])
            p[0] = (
                'multi_blocks',
                block_list
            )
        else:
            raise ValueError('len is %d' % len(p))

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_block(self, p):
        '''
            block : expression
        '''
        p[0] = p[1]

    def p_one_item_expression(self, p):
        '''
            expression : number
                       | assign
                       | keyword
        '''
        p[0] = p[1]

    def p_three_items_expression(self, p):
        '''
            expression : expression '+' expression
                       | expression '-' expression
                       | expression '*' expression
                       | expression '/' expression
        '''
        p[0] = (
            'expression',
            ('operator', p[2]),
            p[1],
            p[3]
        )

    def p_number(self, p):
        '''
            number : NUMBER
        '''
        p[0] = ('number', p[1])

    def p_keyword(self, p):
        '''
            keyword : KEYWORD
        '''
        p[0] = ('keyword', p[1])

    def p_simple_assign(self, p):
        '''
            assign : keyword '=' expression
        '''
        p[0] = (
            'assign',
            p[1],
            p[3]
        )
