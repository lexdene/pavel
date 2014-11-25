from .parser import Parser
from . import lang_structs


def execute_code(source, **options):
    parser = Parser()
    parse_tree = parser.parse(source)

    lang = lang_structs.create(parse_tree)
    env = {}
    result = lang.execute(env)

    return result
