from ply import yacc

from . import lexer


class Parser:
    def __init__(self):
        self._debug = False

        import os
        if os.environ.get('PARSER_DEBUG') == 'on':
            self._debug = True

    def _create_lexer(self):
        return lexer.Lexer()

    def parse(self, source):
        if self._debug:
            self._debug_parse_tokens(source)
            parser = yacc.yacc(module=self)
        else:
            parser = yacc.yacc(module=self, debug=False, write_tables=False)

        return parser.parse(
            source,
            lexer=self._create_lexer()
        )

    def _debug_parse_tokens(self, source):
        _lexer = self._create_lexer()
        print(' ==== debug begin ==== ')

        print(_lexer.tokens)

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
        ('left', 'GT', 'LT', 'GTE', 'LTE'),
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
            block : line
        '''
        p[0] = p[1]

    def p_line(self, p):
        '''
            line : expression NEWLINE
                 | if_struct NEWLINE
                 | if_with_else_struct NEWLINE
                 | while_struct NEWLINE
                 | function_struct NEWLINE
        '''
        p[0] = p[1]

    def p_one_item_expression(self, p):
        '''
            expression : number
                       | keyword
                       | function_call
                       | anonymous_function_struct NEWLINE
        '''
        p[0] = p[1]

    def p_three_items_expression(self, p):
        '''
            expression : expression '+' expression
                       | expression '-' expression
                       | expression '*' expression
                       | expression '/' expression
                       | expression GT expression
                       | expression LT expression
                       | expression GTE expression
                       | expression LTE expression
                       | expression EQUAL expression
                       | keyword ASSIGN expression
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

    def p_if_struct(self, p):
        '''
            if_struct : IF expression INDENT multi_blocks OUTDENT
        '''
        p[0] = (
            'if_struct',
            p[2],
            p[4],
            None,
        )

    def p_if_with_block(self, p):
        '''
            if_struct : IF INDENT multi_blocks OUTDENT NEWLINE THEN INDENT multi_blocks OUTDENT
        '''
        p[0] = (
            'if_struct',
            p[3],
            p[8],
            None
        )

    def p_if_with_else(self, p):
        '''
            if_with_else_struct : if_struct NEWLINE ELSE INDENT multi_blocks OUTDENT
        '''
        p[0] = (
            'if_struct',
            p[1][1],
            p[1][2],
            p[5],
        )

    def p_while_struct(self, p):
        '''
            while_struct : WHILE expression INDENT multi_blocks OUTDENT
        '''
        p[0] = (
            'while_struct',
            p[2],
            p[4],
        )

    def p_function_struct(self, p):
        '''
            function_struct : FUNCTION keyword '(' formal_param_list ')' INDENT multi_blocks OUTDENT
        '''
        p[0] = (
            'function_struct',
            p[2],
            p[4],
            p[7],
        )

    def p_formal_param_list_with_one_item(self, p):
        '''
            formal_param_list : keyword
        '''
        p[0] = (
            'formal_param_list',
            [p[1]]
        )

    def p_formal_param_list_with_multi_items(self, p):
        '''
            formal_param_list : formal_param_list ',' keyword
        '''
        formal_param_list = p[1][1]
        formal_param_list.append(p[3])

        p[0] = (
            'formal_param_list',
            formal_param_list
        )

    def p_function_call(self, p):
        '''
            function_call : keyword '(' comma_expression_list ')'
        '''
        p[0] = (
            'function_call',
            p[1],
            p[3],
        )

    def p_actual_param_list_with_one_item(self, p):
        '''
            comma_expression_list : expression
        '''
        p[0] = (
            'comma_expression_list',
            [p[1]],
        )

    def p_actual_param_list_with_multi_items(self, p):
        '''
            comma_expression_list : comma_expression_list ',' expression
        '''
        exp_list = p[1][1]
        exp_list.append(p[3])
        p[0] = (
            'comma_expression_list',
            exp_list,
        )

    def p_anonymous_function_struct(self, p):
        '''
            anonymous_function_struct : FUNCTION '(' formal_param_list ')' INDENT multi_blocks OUTDENT
        '''
        p[0] = (
            'function_struct',
            None,
            p[3],
            p[6]
        )
