from .grammar.parser import Parser
from .grammar.abstract_syntax_tree import create as create_ast
from .runtime.scope import Scope
from .runtime.buildins import buildins


def execute_code(source, **options):
    parser = Parser()
    parse_tree = parser.parse(source)
    ast = create_ast(parse_tree)

    scope = Scope()

    # fill buildins in top scope
    for key, value in buildins.items():
        scope[key] = value

    result = ast.execute(scope)
    return result, scope
