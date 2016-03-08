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
            self.__parser = yacc.yacc(module=self)

            debug = 0
        else:
            self.__parser = yacc.yacc(
                module=self,
                debug=False,
                write_tables=False
            )

            debug = 0

        result = self.__parser.parse(
            source,
            lexer=self._create_lexer(),
            debug=debug
        )

        if self._debug:
            import pprint
            pprint.pprint(result, indent=4)

        return result

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
        ('nonassoc', 'CMP'),
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def p_first_rule(self, p):
        '''
            first_rule : multi_lines
        '''
        p[0] = p[1]

    def p_error(self, p):
        raise ValueError(p)

    def p_multi_lines(self, p):
        '''
            multi_lines : empty
                        | line
                        | multi_lines line
        '''
        if len(p) == 2:
            if p[1] is None:
                p[0] = (
                    'multi_lines',
                    dict(
                        lines=[]
                    ),
                )
            else:
                p[0] = (
                    'multi_lines',
                    dict(
                        lines=[p[1]]
                    ),
                )
        elif len(p) == 3:
            line_list = p[1][1]['lines'] + [p[2]]
            p[0] = (
                'multi_lines',
                dict(
                    lines=line_list
                ),
            )
        else:
            raise ValueError('len is %d' % len(p))

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_line(self, p):
        '''
            line : expression NEWLINE
                 | assign NEWLINE
                 | if_struct NEWLINE
                 | for_struct NEWLINE
                 | while_struct NEWLINE
                 | function_struct NEWLINE
        '''
        p[0] = p[1]

    def p_one_item_expression(self, p):
        '''
            expression : number
                       | keyword
                       | string
                       | function_call
                       | member_function_call
                       | anonymous_function_struct
                       | block
        '''
        p[0] = p[1]

    def p_three_items_expression(self, p):
        '''
            expression : expression '+' expression
                       | expression '-' expression
                       | expression '*' expression
                       | expression '/' expression
                       | expression CMP expression
        '''
        p[0] = (
            'expression',
            dict(
                operator=('operator', p[2]),
                args=(
                    p[1],
                    p[3]
                )
            )
        )

    def p_keyword_expression(self, p):
        '''
            expression : expression keyword expression
        '''
        p[0] = (
            'function_call',
            dict(
                function=p[2],
                params=[
                    p[1],
                    p[3],
                ]
            )
        )

    def p_assign(self, p):
        '''
            assign : keyword ASSIGN expression
        '''
        p[0] = (
            'expression',
            dict(
                operator=('operator', p[2]),
                args=(
                    p[1],
                    p[3]
                )
            )
        )

    def p_get_attr_expression(self, p):
        '''
            expression : expression '.' keyword
        '''
        p[0] = (
            'expression',
            dict(
                operator=('operator', p[2]),
                args=(
                    p[1],
                    p[3]
                )
            )
        )

    def p_set_attr_expression(self, p):
        '''
            expression : expression '.' keyword ASSIGN expression
        '''
        p[0] = (
            'expression',
            dict(
                operator=('operator', 'set_attr'),
                args=(
                    p[1],
                    p[3],
                    p[5],
                )
            )
        )

    def p_get_item_expression(self, p):
        '''
            expression : expression '[' expression ']'
        '''
        p[0] = (
            'expression',
            dict(
                operator=('operator', p[2] + p[4]),
                args=(
                    p[1],
                    p[3]
                )
            )
        )

    def p_number(self, p):
        '''
            number : NUMBER
        '''
        p[0] = ('number', dict(number=p[1]))

    def p_keyword(self, p):
        '''
            keyword : KEYWORD
        '''
        p[0] = (
            'keyword',
            dict(
                name=p[1]
            )
        )

    def p_string(self, p):
        '''
            string : STRING
        '''
        p[0] = ('string', dict(string=p[1][1:-1]))

    def p_if_struct(self, p):
        '''
            if_struct : IF '(' expression ')' INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'if_struct',
            dict(
                condition=p[3],
                then_block=p[6],
                else_block=None,
            )
        )

    def p_if_with_block(self, p):
        '''
            if_struct : IF INDENT multi_lines OUTDENT NEWLINE THEN INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'if_struct',
            dict(
                condition=p[3],
                then_block=p[8],
                else_block=None
            )
        )

    def p_if_with_else(self, p):
        '''
            if_struct : if_struct NEWLINE ELSE INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'if_struct',
            dict(
                condition=p[1][1]['condition'],
                then_block=p[1][1]['then_block'],
                else_block=p[5],
            )
        )

    def p_for_struct(self, p):
        '''
            for_struct : FOR '(' keyword IN expression ')' INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'for_struct',
            dict(
                keyword=p[3],
                expression=p[5],
                body=p[8],
            )
        )

    def p_while_struct(self, p):
        '''
            while_struct : WHILE '(' expression ')' block
        '''
        p[0] = (
            'while_struct',
            dict(
                condition=p[3],
                body=p[5],
            )
        )

    def p_function_struct(self, p):
        '''
            function_struct : FUNCTION keyword '(' formal_param_list ')' INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'function_struct',
            dict(
                name=p[2],
                params=p[4],
                body=p[7],
            )
        )

    def p_no_param_function_struct(self, p):
        '''
            function_struct : FUNCTION keyword '(' ')' INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'function_struct',
            dict(
                name=p[2],
                params=[],
                body=p[6],
            )
        )

    def p_formal_param_list_with_one_item(self, p):
        '''
            formal_param_list : keyword
        '''
        p[0] = [p[1]]

    def p_formal_param_list_with_multi_items(self, p):
        '''
            formal_param_list : formal_param_list ',' keyword
        '''
        formal_param_list = p[1]
        formal_param_list.append(p[3])

        p[0] = p[1] + [p[3]]

    def p_member_function_call(self, p):
        '''
            member_function_call : expression '.' keyword '(' comma_expression_list ')'
        '''
        p[0] = (
            'member_function_call',
            dict(
                this_object=p[1],
                name=p[3],
                params=p[5],
            )
        )

    def p_no_param_member_function_call(self, p):
        '''
            member_function_call : expression '.' keyword '(' ')'
        '''
        p[0] = (
            'member_function_call',
            dict(
                this_object=p[1],
                name=p[3],
                params=[],
            )
        )

    def p_function_call(self, p):
        '''
            function_call : expression '(' comma_expression_list ')'
        '''
        p[0] = (
            'function_call',
            dict(
                function=p[1],
                params=p[3],
            )
        )

    def p_no_param_function_call(self, p):
        '''
            function_call : expression '(' ')'
        '''
        p[0] = (
            'function_call',
            dict(
                function=p[1],
                params=[]
            )
        )

    def p_call_block(self, p):
        '''
            function_call : expression block
        '''
        p[0] = (
            'function_call',
            dict(
                function=p[1],
                params=[p[2]]
            )
        )

    def p_actual_param_list_with_one_item(self, p):
        '''
            comma_expression_list : expression
        '''
        p[0] = [p[1]]

    def p_actual_param_list_with_multi_items(self, p):
        '''
            comma_expression_list : comma_expression_list ',' expression
                                  | comma_expression_list ',' expression NEWLINE
        '''
        p[0] = p[1] + [p[3]]

    def p_anonymous_function_struct(self, p):
        '''
            anonymous_function_struct : FUNCTION '(' formal_param_list ')' INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'function_struct',
            dict(
                name=None,
                params=p[3],
                body=p[6]
            )
        )

    def p_anonymous_function_without_param(self, p):
        '''
            anonymous_function_struct : FUNCTION '(' ')' INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'function_struct',
            dict(
                name=None,
                params=[],
                body=p[5],
            )
        )

    def p_anonymous_function_struct_without_param(self, p):
        '''
            block : INDENT multi_lines OUTDENT
        '''
        p[0] = (
            'function_struct',
            dict(
                name=None,
                params=[],
                body=p[2]
            )
        )
