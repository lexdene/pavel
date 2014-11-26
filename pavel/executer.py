from .parser import Parser
from . import lang_structs
from . import runtime_env


def execute_code(source, **options):
    parser = Parser()
    parse_tree = parser.parse(source)

    lang = lang_structs.create(parse_tree)
    env = runtime_env.Env()
    result = lang.execute(env)

    return result
